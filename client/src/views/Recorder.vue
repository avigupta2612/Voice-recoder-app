<template>
  <div>
    <h1 class="mb-2">VOICE RECORDER</h1>
    <CCard>
      <CCardBody>
        <div class="record-box">
          <img
            src="../assets/pages/microphone.png"
            height="auto"
            width="80px"
            v-if="!recordingInProcess"
          />
          <h1 v-else class="mb-base text-white">
            {{ prettyTime | prettify }}
          </h1>
        </div>
      </CCardBody>
      <CCardFooter>
        <CButton
          v-if="!recordingInProcess"
          color="primary"
          @click="startRecording"
          >Start Recording</CButton
        >
        <CButton v-else color="danger" @click="stopRecording"
          >Stop Recording</CButton
        >
      </CCardFooter>
    </CCard>
    <CCard>
      <CCardHeader class="text-left"> Recordings </CCardHeader>
      <CCardBody>
        <CDataTable
          hover
          :items="this.recordingList"
          :fields="getRecordingListHeaders"
        >
          <template #audio="{ item }">
            <td class="py-2">
              <audio controls :src="getUrl(item.inputFile)" />
            </td>
          </template>
          <template #outputAudio="{ item }">
            <td class="py-2 postion-relative">
              <div v-if="!item.outputFile">
                <CSpinner color="info"/>
              </div>
              <audio v-else controls src=""/>
            </td>
          </template>
        </CDataTable>
      </CCardBody>
    </CCard>
  </div>
</template>
<script>
const MicRecorder = require("mic-recorder-to-mp3");
import { ajaxCallMixin } from "@/mixins/HttpCommon";
export default {
  name: "Recorder",
  mixins: [ajaxCallMixin],
  data() {
    return {
      fileName: "",
      fields: [],
      recordingInProcess: false,
      recorder: null,
      recordingReady: false,
      audioBlob: null,
      audioFile: null,
      isRunning: true,
      recordingCount: 1,
      uploadInProgress: false,  
      minutes: 0,
      secondes: 0,
      time: 0,
      timer: null,
      recordingList: [],
    };
  },
  filters: {
    prettify: function (value) {
      const data = value.split(":");
      let minutes = data[0];
      let secondes = data[1];
      if (minutes < 10) {
        minutes = "0" + minutes;
      }
      if (secondes < 10) {
        secondes = "0" + secondes;
      }
      return minutes + ":" + secondes;
    },
  },
  computed: {
    prettyTime() {
      const time = this.time / 60;
      const minutes = parseInt(time);
      const secondes = Math.round((time - minutes) * 60);
      return minutes + ":" + secondes;
    },
    getRecordingListHeaders() {
      return [
        { key: "name", label: "Name", filter: false },
        { key: "audio", label: "Input Audio", filter: false },
        { key: "outputAudio", label: "Output Audio", filter: false },
      ];
    },
  },
  mounted() {
    this.recorder = new MicRecorder({
      bitRate: 128,
    });
  },
  methods: {
    getUrl(file) {
      return URL.createObjectURL(file);
    },
    startRecording() {
      this.recorder
        .start()
        .then(() => {
          this.startTimer();
          this.recordingInProcess = true;
        })
        .catch((e) => {
          console.error(e);
        });
    },
    stopRecording() {
      this.recorder
        .stop()
        .getMp3()
        .then(([buffer, blob]) => {
          this.resetTimer();

          this.recordingInProcess = false;
          const audioFile = new File(
            buffer,
            `recording_${this.recordingCount}.mp3`,
            {
              type: blob.type,
              lastModified: Date.now(),
            }
          );
          console.log(audioFile);
          this.handleUpload(audioFile,this.recordingCount -1);
          this.recordingList.push({
            name: `Recording-${this.recordingCount}`,
            inputFile: audioFile,
            //createdAt: audioFile.lastModifiedDate.toLocaleTimeString(),
            outputFile: null,
          });
          this.recordingCount++;
        });
    },
    startTimer() {
      this.isRunning = true;
      if (!this.timer) {
        this.timer = setInterval(() => {
          this.time++;
          /* if (this.time > 0) {
            this.time++
          } else {
            clearInterval(this.timer)
            //this.sound.play()
            this.reset()
          } */
        }, 1000);
      }
    },
    stopTimer() {
      this.isRunning = false;
      clearInterval(this.timer);
      this.timer = null;
    },
    resetTimer() {
      this.stopTimer();
      this.time = 0;
      this.secondes = 0;
      this.minutes = 0;
    },
    handleUpload(file, index) {
      this.fields["audio_data"] = file;
      this.uploadInProgress = true;
      console.log(index);
      setTimeout(()=> {
        this.recordingList[index].outputFile = true;
      },5000);
     /* const url = "/upload_audio";
      const data = { recordingId: index };
      this.ajaxCall(url, data, this.handleUploadResponse, this.fields); */
    },
    handleUploadResponse(apiResponse) {
      console.log(apiResponse);
    },
  },
};
</script>
<style scoped>
.record-box {
  height: 200px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 1rem;
  background: #314755; /* fallback for old browsers */
  background: -webkit-linear-gradient(
    to right,
    #26a0da,
    #314755
  ); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(
    to right,
    #26a0da,
    #314755
  ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>