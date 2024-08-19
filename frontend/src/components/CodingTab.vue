<template>
  <ul class="list-group mt-3">
    <li v-for="code in course.codingqs" :key="code.id" class="list-group-item">
      <router-link :to="'/code/' + code.id"> 
        <p style="font-weight: bold;">{{ code.title }}</p>
        <p>{{ code.description }}</p>
      </router-link>
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
