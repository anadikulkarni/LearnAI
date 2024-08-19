<template>
    <div v-for="transcript in lecture_transcripts" :key="transcript.id" class="mb-3 mt-3">
      <h4>Transcript for: {{ transcript.title }}</h4>
      <p>{{ transcript.content }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        lecture_transcripts: []  // Initialize the array to store transcripts
      };
    },
    props: {
      course: {
        type: Object,
        required: true
      }
    },
    methods: {
    getVideoId(url) {
      const match = url.match(/v=([^&]+)/);
      return match ? match[1] : null;
    },

    async getAllTranscripts() {
      this.lecture_transcripts = [];  // Clear any existing transcripts
      for (const video of this.course.videos) {
        const videoId = this.getVideoId(video.url);
        if (videoId) {
          try {
            const response = await fetch(`http://127.0.0.1:5000/api/transcript/${videoId}?course_id=${this.course.id}`);
            const data = await response.json();
            this.lecture_transcripts.push({
              id: videoId,
              title: video.title,
              content: data.transcript
            });
          } catch (error) {
            console.error(`Error fetching transcript for video ${videoId}:`, error);
          }
        }
      }
      console.log(this.lecture_transcripts);
    }
  },
  mounted() {
    this.getAllTranscripts();  // Fetch transcripts when the component is mounted
  }
  };
  </script>