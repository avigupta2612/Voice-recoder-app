import torch
import torch.nn as nn
import numpy as np
import segmentation_models_pytorch as smp
import os
from demobackend.settings import BASE_DIR
from transformers import Speech2TextForConditionalGeneration, Speech2TextProcessor
from preprocess import s2t_audio_to_array

def conv_block(no_layers, inp_filters, no_filters):
    layers=[]
    layers.append(nn.Conv2d(inp_filters, no_filters, 3, padding=1))
    layers.append(nn.BatchNorm2d(no_filters))
    layers.append(nn.LeakyReLU(0.1, inplace=True))
    for i in range(no_layers-1):
        layers.append(nn.Conv2d(no_filters, no_filters, 3, padding=1))
        layers.append(nn.BatchNorm2d(no_filters))
        layers.append(nn.LeakyReLU(0.1, inplace=True))
    layers.append(nn.MaxPool2d(2,2))
    return nn.Sequential(*layers)

def t_conv_block(no_layers, inp_filters, no_filters):
    layers=[]
    layers.append(nn.ConvTranspose2d(inp_filters, no_filters, 2, stride=2))
    for i in range(no_layers-1):
        layers.append(nn.Conv2d(no_filters, no_filters, 3, padding=1))
        layers.append(nn.BatchNorm2d(no_filters))
        layers.append(nn.LeakyReLU(0.1, inplace=True))
    
    return nn.Sequential(*layers)

class DenoisingModel(nn.Module):
    def __init__(self, no_filters):
        super(DenoisingModel, self).__init__()
        self.conv1 = conv_block(3, 1, no_filters)
        self.conv2 = conv_block(3, no_filters, no_filters*2)
        self.conv3 = conv_block(3, no_filters*2, no_filters*4)
        self.conv4 = conv_block(3, no_filters*4, no_filters*8)
        self.tconv1 = t_conv_block(3, no_filters*8, no_filters*4)
        self.tconv2 = t_conv_block(3, no_filters*4, no_filters*2)
        self.tconv3 = t_conv_block(3, no_filters*2, no_filters)
        self.tconv4 = nn.Sequential(nn.ConvTranspose2d(no_filters, no_filters,2, stride=2),
                                    nn.BatchNorm2d(no_filters),
                                    nn.Conv2d(no_filters, no_filters,3, padding=1),
                                    nn.BatchNorm2d(no_filters),
                                    nn.LeakyReLU(0.1, inplace=True),
                                    nn.Conv2d(no_filters, 1,3, padding=1),
                                    nn.Tanh())
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.tconv1(x)
        x = self.tconv2(x)
        x = self.tconv3(x)
        x = self.tconv4(x)
        return x

def model_out(spec_array, model='unet'):
    train_on_gpu = True if torch.cuda.is_available() else False
    cnn_auto_path = r'C:\Users\Avi\Desktop\speech denoising\model.pt'
    unet_path = os.path.join(BASE_DIR, 'speech_models', 'unet-1.pt')

    if model == 'cnn-auto':
        cnn_auto_model = DenoisingModel(64)
        cnn_auto_model.load_state_dict(torch.load(cnn_auto_path))
        model_inp = torch.from_numpy(spec_array)
        if train_on_gpu:
            cnn_auto_model.cuda()
            model_inp = model_inp.cuda()
        model_out = cnn_auto_model(model_inp.float())
        output = model_inp().numpy().squeeze() - model_out().detach().cpu().numpy().squeeze()
        return output
    else:
        unet = torch.load(unet_path, map_location=torch.device('cpu'))
        model_inp = torch.from_numpy(spec_array)
        if train_on_gpu:
            unet.cuda()
            model_inp = model_inp.cuda()
        model_out = unet(model_inp.float())
        output = model_inp.numpy().squeeze() - model_out.detach().cpu().numpy().squeeze()
        return output

def s2t_predictions(audio_file):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    audio_array = s2t_audio_to_array(audio_file)
    model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr").to(device).eval()
    processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr", do_upper_case=True)
    features = processor(audio_array, sampling_rate=16000, return_tensors="pt")
    input_features = features.input_features.to(device)
    attention_mask = features.attention_mask.to(device)
    gen_tokens = model.generate(input_ids=input_features)
    text = processor.batch_decode(gen_tokens, skip_special_tokens=True)
    return text