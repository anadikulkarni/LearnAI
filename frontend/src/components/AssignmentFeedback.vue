<template>
    <div class="card mb-3">
      <div class="card-body">
        <p class="card-text">{{ feedback.feedback }}</p>
        <p class="card-text text-muted">
          Submitted on: {{ formatDate(feedback.created_at) }}
          <span v-if="canDelete" class="float-right">
            <button @click="deleteFeedback" class="btn btn-sm btn-danger">
              Delete
            </button>
          </span>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import fetchUtil from '../FetchUtil.js';
  import store from '../store';
  
  export default {
    props: {
      feedback: {
        type: Object,
        required: true,
      },
    },
    computed: {
      canDelete() {
        const user = store.state.currentUser;
        return user && (user.roles.includes('admin') || user.roles.includes('instructor'));
      },
    },
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
      },
      async deleteFeedback() {
        try {
          await fetchUtil({
            endpoint: `assignment_feedback/${this.feedback.id}`,
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            user_id: store.state.currentUser,
          });
          this.$emit('feedback-deleted'); // Emit an event to notify the parent component
        } catch (error) {
          console.error('Error deleting feedback:', error);
          // Handle error (e.g., display an error message)
        }
      },
    },
  };
  </script>