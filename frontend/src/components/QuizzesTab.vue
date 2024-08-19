<template>
  <ul class="list-group mt-3">
    <li v-for="quiz in course.quizzes" :key="quiz.id" class="list-group-item">
      <router-link :to="'/quiz/' + quiz.id"> 
        <p style="font-weight: bold;">{{ quiz.title }}</p>
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
