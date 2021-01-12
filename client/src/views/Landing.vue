<template>
  <div>
    <div class="d-flex justify-content-center">
      <CCard class="w-50">
        <CCardBody>
          <CRow align-horizontal="center">
            <CCol class="col-2">
                <CButton color="primary" size="lg" @click="$router.push('/upload')">Upload</CButton>
            </CCol>
            <CCol class="col-2">
                <CButton color="primary" size="lg">Record</CButton>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </div>
  </div>
</template>
<script>
export default {
  name: "Landing",
};
</script>