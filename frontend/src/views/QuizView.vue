<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0">
            <router-link to="/">Home</router-link>
            <span class="mx-2 mb-0">/</span>
            <strong class="text-black">Quiz</strong>
            <span class="mx-2 mb-0">/</span>
            <strong class="text-black" v-if="quiz">{{ quiz.title }}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="site-section" v-if="!quizSubmitted">
      <div class="container" v-if="quiz">
        <div class="row mb-5">
          <div class="col-md-8">
            <h2 class="text-black h5 mb-3">{{ quiz.title }}</h2>
            <p class="text-muted">
              This quiz belongs to the course:
              <strong>
                <router-link :to="'/course/' + quiz.course.id">{{ quiz.course.title }}</router-link>
              </strong>
            </p>
            <p class="text-muted">Created on: {{ formatDate(quiz.created_at) }}</p>

            <div v-for="(question, index) in quiz.questions" :key="question.id" class="mb-4">
              <h5>{{ index + 1 }}. {{ question.content }}</h5>
              <ul class="list-group">
                <li v-for="option in question.options" :key="option.id" class="list-group-item">
                  <label>
                    <input
                      type="radio"
                      :name="`question-${question.id}`"
                      :value="option.id"
                      v-model="selectedAnswers[question.id]"
                    />
                    {{ option.content }}
                  </label>
                </li>
              </ul>
            </div>
          </div>

          <div class="col-md-4">
            </div>
        </div>
        <button class="btn btn-primary" @click="submitQuiz">Submit Quiz</button>
      </div>
      <div v-else-if="isLoading">
        <p>Loading quiz details...</p>
      </div>
      <div v-else>
        <p>Error loading quiz. Please try again later.</p>
      </div>
    </div>

    <div v-else>
      <div class="container mt-5">
        <h2>Quiz Results</h2>
        <h2 class="text-black h5 mb-3">{{ quiz.title }}</h2>
            <p class="text-muted">
              This quiz belongs to the course:
              <strong>
                <router-link :to="'/course/' + quiz.course.id">{{ quiz.course.title }}</router-link>
              </strong>
            </p>
        <p>Your Score: {{ quizResult.score }}%</p>
        <p>Submitted on: {{ formatDate(quizResult.created_at) }}</p>
      </div>
    </div>

    <FooterItem />
  </div>
</template>

<script>
import FooterItem from '../components/FooterItem.vue';
import fetchUtil from '../FetchUtil.js';
import store from '../store';
import { RouterLink } from 'vue-router';

export default {
  components: {
    FooterItem,
    RouterLink,
  },
  data() {
    return {
      quiz: null,
      quizId: this.$route.params.id,
      selectedAnswers: {},
      quizSubmitted: false,
      quizResult: null,
      isLoading: true, // Add isLoading flag
    };
  },
  mounted() {
    this.fetchQuizData();
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    async fetchQuizData() {
      this.isLoading = true; // Set isLoading to true while fetching
      try {
        const response = await fetchUtil({
          endpoint: `quizzes/${this.quizId}`,
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: store.state.currentUser,
        });
        this.quiz = response;

        // Check if the user has already submitted the quiz
        this.quizResult = this.quiz.results.find(
          (result) => result.user_id === 3 // Replace with actual user ID
        );

        if (this.quizResult) {
          this.quizSubmitted = true;
        }
      } catch (error) {
        console.error('Error fetching quiz details:', error);
      } finally {
        this.isLoading = false; // Set isLoading to false regardless of outcome
      }
    },

    async submitQuiz() {
      if (Object.keys(this.selectedAnswers).length === 0) {
        alert('Please select at least one answer before submitting.');
        return;
      }

      try {
        const response = await fetchUtil({
          endpoint: `submit_quiz/${this.quizId}`,
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: { answers: this.selectedAnswers },
        });

        // Update quiz results and set quizSubmitted to true
        this.quiz.results = [response];
        this.quizResult = response;
        this.quizSubmitted = true;
        console.log('Quiz submitted successfully:', response);
      } catch (error) {
        console.error('Error submitting quiz:', error);
      }
    },
  },
};
</script>