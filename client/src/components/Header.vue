<template>
  <CHeader fixed class="p-2">
    <CHeaderBrand class="flex align-items-center" href="/">
      <img src="../assets/Critical_Frequency_Logo.png" height="40px" width="40px">
      <h3 class="mb-0 ml-2">DeepNoise</h3>
    </CHeaderBrand>
    <CHeaderNav class="justify-content-end flex-grow-1">
      <CHeaderNavLink to="/">Home</CHeaderNavLink>
      <CHeaderNavLink to="/upload">Upload</CHeaderNavLink>
      <CHeaderNavLink to="/samples">Samples</CHeaderNavLink>
    </CHeaderNav>
  </CHeader>
</template>
<script>
export default {
  name: "Header",
};
</script>