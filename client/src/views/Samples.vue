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
            <audio controls :src="getUrl(item.noiseTypeinputFile)" />
          </td>
        </template>
        <template #outputAudio="{ item }">
          <td class="py-2 postion-relative">
            <audio controls :src="getUrl(item.File)" />
          </td>
        </template>
      </CDataTable>
    </CCardBody>
  </CCard>
</template>
<script>
export default {
  name: "Samples",
  data() {
      return {
        sampleRecordingList: [
            //{noiseType:"Siren",audio:"",outputAudio:""},
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
  },
  methods: {

  },
};
</script>