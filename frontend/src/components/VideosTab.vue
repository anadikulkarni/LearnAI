<script setup>
import { RouterLink, RouterView } from 'vue-router'
import quiz_Sidebar from './Interactive_quiz.vue'
import { ref, onMounted } from 'vue';

const isSidebar3Expanded = ref(true);
const sidebar3Ref = ref(null);

onMounted(() => {
  // Sync with the initial state of the sidebar from localStorage
  isSidebar3Expanded.value = localStorage.getItem("is_q_expanded") === "true";
});

const toggleSidebar3 = () => {
  console.log("toggled Quiz Sidebar");
  isSidebar3Expanded.value = !isSidebar3Expanded.value;
  localStorage.setItem("is_q_expanded", isSidebar3Expanded.value);
  // Ensure the Sidebar component reacts accordingly
  if (isSidebar3Expanded.value) {
    sidebar3Ref.value.ToggleMenu();
  } else {
    sidebar3Ref.value.ToggleMenu();
  }
};
</script>

<template>
  <quiz_Sidebar :key="isSidebar3Expanded" :is_1_expanded="isSidebar3Expanded" ref="sidebar3Ref"/>
  <div class="mt-3">
    <p style="color: red;"><b>To discuss a lecture with Learn AI Assistant or to Attempt an interactive quiz, first select the lecture!</b></p>
    <div v-for="video in course.videos" :key="video.yt_id" :class="['card', 'mb-3', { 'selected': selectedVideoId === video.yt_id }]">
      <div class="row no-gutters">
        <div class="col-md-auto">
          <a :href="video.url" target="_blank">
            <img
              :src="'https://img.youtube.com/vi/' + getVideoId(video.url) + '/0.jpg'" 
              class="card-img"
              alt="Video Thumbnail"
              style="max-width: 160px; height: auto;"
            />
          </a>
        </div>
        <div class="col">
          <div class="card-body">
            <a :href="video.url" target="_blank">
              <h5 class="card-title">{{ video.title }}</h5>
            </a>
            <button
              @click="selectVideo(video.yt_id)"
              class="btn btn-primary"
              :class="{ 'btn-success': selectedVideoId === video.yt_id }"
            >
              {{ selectedVideoId === video.yt_id ? 'Selected' : 'Select' }}
            </button>
            <a :href="video.url" target="_blank"><button class="btn btn-primary ml-10">Watch</button></a>
          </div>
        </div>
      </div>
    </div>
    <button @click="toggleSidebar3" class="btn btn-dark quizbtn"  style="margin-right: 10px; margin-top: 10px; margin-bottom: 10px; padding:15px 20px;">Attempt Interactive Quiz</button>
  </div>
</template>

<script>
export default {
  props: {
    course: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedVideoId: null  // Track the selected video ID
    };
  },
  methods: {
    getVideoId(url) {
      // Simple regex to extract YouTube video ID
      const match = url.match(/v=([^&]+)/); 
      return match ? match[1] : null;
    },
    selectVideo(videoId) {
      // Toggle the selected video ID
      if (this.selectedVideoId === videoId) {
        this.selectedVideoId = null;
        localStorage.removeItem('video_id');
      } else {
        this.selectedVideoId = videoId;
        localStorage.setItem('video_id', videoId);
      }
    }
  },
  mounted() {
    // Set initial video_id and current_course_id in local storage
    localStorage.setItem('current_course_id', this.course.id);
    if (this.course.videos.length > 0) {
      localStorage.setItem('video_id', this.course.videos[0].yt_id);
      this.selectedVideoId = this.course.videos[0].yt_id;
    }
  }
};
</script>

<style>
/* Style for the selected card */
.selected {
  background-color: #d4edda; /* Light green background */
  border-color: #c3e6cb;     /* Green border */
}

.ml-10 {
  margin-left: 10px;
}
</style>
