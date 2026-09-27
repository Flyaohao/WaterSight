<template>
  <div class="search-container">
    <input
      v-model="searchTitle"
      type="text"
      class="search-input"
      placeholder="搜索博客..."
    />
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      searchTitle: "",
    };
  },
  watch: {
    searchTitle(newVal) {
      console.log("搜索标题变更:", newVal);
      this.$root.$emit("blog-search", newVal);
    },
  },
};
</script>

<style>
.search-container {
  margin: 1rem 0;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #4fb6e0;
  box-shadow: 0 0 0 2px rgba(79, 182, 224, 0.2);
}
</style>
