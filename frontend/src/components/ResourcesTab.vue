<template>
    <ul class="list-group mt-3">
      <li v-for="resource in course.resources" :key="resource.id" class="list-group-item">
        <a :href="resource.url" target="_blank">{{ resource.url }}</a>
      </li>
    </ul>
  </template>
  
  <script>
  export default {
    props: {
      course: {
        type: Object,
        required: true
      }
    }
  };
  </script>