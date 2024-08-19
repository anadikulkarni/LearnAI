<template>
    <div>
      <div class="bg-light py-3">
        <div class="container" v-if="assignment">
          <div class="row">
            <div class="col-md-12 mb-0">
              <router-link to="/">Home</router-link>
              <span class="mx-2 mb-0">/</span>
              <router-link :to="'/course/' + assignment.course.id">
                Course
              </router-link>
              <span class="mx-2 mb-0">/</span>
              <strong class="text-black">Assignment</strong>
              <span class="mx-2 mb-0">/</span>
              <strong class="text-black">{{ assignment.title }}</strong>
            </div>
          </div>
        </div>
      </div>
  
      <div class="site-section">
        <div v-if="assignment" class="container">
          <div class="row">
            <div class="col-md-12">
              <h1>{{ assignment.title }}</h1>
              <p class="text-muted">
                This assignment belongs to the course:
                <strong>
                  <router-link :to="'/course/' + assignment.course.id">{{
                    assignment.course.title
                  }}</router-link>
                </strong>
              </p>
              <p>{{ assignment.description }}</p>
  
              <form @submit.prevent="submitFeedback">
                <div class="form-group">
                  <label for="feedback">Your Feedback:</label>
                  <textarea
                    id="feedback"
                    v-model="newFeedback"
                    class="form-control"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <button type="submit" class="btn btn-primary">
                  Submit Feedback
                </button>
              </form>
  
              <h4 class="mt-5">Feedbacks:</h4>
              <AssignmentFeedback
                v-for="feedback in assignmentFeedback"
                :key="feedback.id"
                :feedback="feedback"
                @feedback-deleted="fetchAllAssignmentFeedback"
              />
              <p v-if="assignmentFeedback.length === 0">No feedback yet.</p>
            </div>
          </div>
        </div>
        <div v-else>
          <p>Loading assignment details...</p>
        </div>
      </div>
  
      <FooterItem />
    </div>
  </template>
  
  <script>
  import FooterItem from '../components/FooterItem.vue';
  import AssignmentFeedback from '../components/AssignmentFeedback.vue';
  import fetchUtil from '../FetchUtil.js';
  import store from '../store';
  import { RouterLink } from 'vue-router';
  
  export default {
    components: {
      AssignmentFeedback,
      FooterItem,
      RouterLink,
    },
    data() {
      return {
        assignment: null,
        assignmentFeedback: [],
        assignmentId: this.$route.params.id,
        newFeedback: '',
      };
    },
    mounted() {
      this.fetchAssignmentData();
      this.fetchAllAssignmentFeedback();
    },
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
      },
      async fetchAssignmentData() {
        try {
          const response = await fetchUtil({
            endpoint: `assignments/${this.assignmentId}`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            user_id: store.state.currentUser,
          });
          this.assignment = response;
        } catch (error) {
          console.error('Error fetching assignment details:', error);
        }
      },
      async fetchAllAssignmentFeedback() {
        try {
          const response = await fetchUtil({
            endpoint: `assignments/${this.assignmentId}/feedbacks`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            user_id: store.state.currentUser,
          });
          this.assignmentFeedback = response;
        } catch (error) {
          console.error('Error fetching all assignment feedback:', error);
        }
      },
      async submitFeedback() {
        try {
          await fetchUtil({
            endpoint: 'assignment_feedbacks',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            user_id: store.state.currentUser,
            data: {
              assignment_id: this.assignmentId,
              feedback: this.newFeedback,
            },
          });
  
          this.newFeedback = '';
          this.fetchAllAssignmentFeedback();
        } catch (error) {
          console.error('Error submitting feedback:', error);
        }
      },
    },
  };
  </script>