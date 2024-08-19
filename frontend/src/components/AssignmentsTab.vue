<template>
  <ul class="list-group mt-3">
    <li
      v-for="assignment in course.assignments"
      :key="assignment.id"
      class="list-group-item"
    >
      <router-link :to="'/assignment/' + assignment.id"> 
        <p style="font-weight: bold;">{{ assignment.title }}</p> {{ assignment.description }}
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