<template>
  <CCard>
    <CCardHeader class="text-left">Samples</CCardHeader>
    <CCardBody>
      <CDataTable
        hover
        :items="this.sampleRecordingList"
        :fields="getRecordingListHeaders"
      >
        <template #audio="{ item }">
          <td class="py-2">
            <audio controls :src="getUrl(`${item.noiseType}/originalAudio.wav`)" />
          </td>
        </template>
        <template #outputAudio="{ item }">
          <td class="py-2 postion-relative">
            <audio controls :src="getUrl(`${item.noiseType}/cleanAudio.wav`)" />
          </td>
        </template>
      </CDataTable>
    </CCardBody>
  </CCard>
</template>
<script>
import constants from '../constant';
export default {
  name: "Samples",
  data() {
      return {
        sampleRecordingList: [
            {noiseType:"Children"},
            {noiseType:"Drilling"},
            {noiseType:"Siren"},
            {noiseType:"Street_music"},
        ]
      }
  },
  computed: {
    getRecordingListHeaders() {
      return [
        { key: "noiseType", label: "Noise", filter: false },
        { key: "audio", label: "Original Audio", filter: false },
        { key: "outputAudio", label: "Output Audio", filter: false },
      ];
    },
    baseUrl() {
      return `${constants.apiUrl}/Voice-recoder-app/localDB/samples`;
    }
  },
  methods: {
    getUrl(suffixPath) {
      return this.baseUrl+"/"+suffixPath;
    }
  },
};
</script>