<template>
    <div>
      <div class="bg-light py-3">
        <div class="container" v-if="course">
          <div class="row">
            <div class="col-md-12 mb-0">
              <router-link to="/">Home</router-link>
              <span class="mx-2 mb-0">/</span>
              <strong class="text-black">Course</strong>
              <span class="mx-2 mb-0">/</span>
              <strong class="text-black">{{ course.title }}</strong>
            </div>
          </div>
        </div>
      </div>
  
      <div class="site-section"> 
        <div class="container">
          <div v-if="course" class="row mb-5">
            <div class="col-md-4">
              <img
                :src="'data:;base64,' + course.image"
                class="img-fluid"
                alt="Course Image"
                style="max-width: 300px; height: auto;"
              />
            </div>
            <div class="col-md-8 order-md-2">
              <h2 class="text-black h5 mb-3">{{ course.title }}</h2>
              <p class="card-text mb-4">{{ course.description }}</p>
  
              <p class="mb-0">
                <span class="badge bg-primary mr-2 text-white">Category: {{ course.category.name }}</span>
                <span class="badge bg-secondary text-dark"
                  >Instructor: {{ course.instructor.username || 'Not Assigned' }}</span
                >
              </p>
              <!-- <p class="mb-3">
                <span
                  v-for="rating in course.ratings"
                  :key="rating.id"
                  class="fa fa-star checked"
                  :class="{ 'text-warning': rating.rating >= 3, 'text-muted': rating.rating < 3 }"
                ></span>
                ({{ course.ratings.length }} ratings)
              </p> -->
              <div class="d-flex">
                <div v-if="userLoggedIn">
                <p></p>
                <button 
                  @click="enroll(course.id)" 
                  :class="user_enrolled.includes(course.id) ? 'btn btn-secondary' : 'btn btn-primary'" 
                  :disabled="user_enrolled.includes(course.id)">
                  {{ user_enrolled.includes(course.id) ? 'ENROLLED' : 'ENROLL' }}
                </button>
                </div>
                <div v-else>
                <p></p>
                <button @click="altenroll" class="btn btn-primary">ENROLL</button>
                </div>
              </div>
            </div>
          </div>
  
          <div v-if="course" class="row mb-5">
            <div class="col-md-12">
              <ul class="nav nav-tabs" id="courseTabs" role="tablist">
                <li class="nav-item" role="presentation" v-for="tab in tabs" :key="tab.id">
                  <button
                    class="nav-link"
                    :class="{ active: activeTab === tab.id }"
                    :id="`${tab.id}-tab`"
                    @click="activeTab = tab.id"
                    type="button"
                    role="tab"
                    :aria-controls="tab.id"
                    :aria-selected="activeTab === tab.id"
                  >
                    {{ tab.name }}
                  </button>
                </li>
              </ul>
  
              <div class="tab-content" id="courseTabsContent">
                <div
                  v-for="tab in tabs"
                  :key="tab.id"
                  class="tab-pane fade"
                  :class="{ 'show active': activeTab === tab.id }"
                  :id="tab.id"
                  role="tabpanel"
                  :aria-labelledby="`${tab.id}-tab`"
                >
                  <component :is="tab.component" :course="course" />
                </div>
              </div>
            </div>
          </div>
  
          <div v-else>
            <p>Loading course details...</p>
          </div>
        </div>
      </div>
  
      <FooterItem /> 
    </div>
  </template>
  
  <script>
  import { RouterLink } from 'vue-router'
  import store from '../store'
  import FooterItem from '../components/FooterItem.vue'
  import Request from '../components/RequestItem.vue';
  import fetchUtil from '../FetchUtil.js';
  import VideosTab from '../components/VideosTab.vue';
  import TranscriptsTab from '../components/TranscriptsTab.vue';
  import AssignmentsTab from '../components/AssignmentsTab.vue';
  import ResourcesTab from '../components/ResourcesTab.vue';
  import QuizzesTab from '../components/QuizzesTab.vue';
  import CodingTab from '../components/CodingTab.vue';
  
  export default {
    data() {
      return {
        course: null,
        courseId: this.$route.params.id,
        user_id: store.state.currentUser,
        messages: [],
        activeTab: 'videos', 
        userLoggedIn: true,
        user_enrolled: [],
        tabs: [
          { id: 'videos', name: 'Lecture Videos', component: VideosTab },
          { id: 'transcripts', name: 'Lecture Transcripts', component: TranscriptsTab },
          { id: 'assignments', name: 'Assignments', component: AssignmentsTab },
          { id: 'resources', name: 'Resources', component: ResourcesTab },
          { id: 'quizzes', name: 'Quizzes', component: QuizzesTab },
          { id: 'coding', name: 'Lab Assignments', component: CodingTab },
        ]
      };
    },
    mounted() {
      this.fetchCourseDetails(this.courseId);
    },
    components: {
      RouterLink,
      Request,
      FooterItem,
      VideosTab,
      TranscriptsTab,
      AssignmentsTab,
      ResourcesTab,
      QuizzesTab,
      CodingTab,
    },
    beforeMount(){
    this.checkCurrentUser();
    },
    methods: {
      altenroll(){
      this.$router.push({ path: '/login', query: { message: "Please login to start enrolling!" } });
      // this.$router.push({ path: `course/${this.courses[0].id}`});
      },
      async enroll(course_id){
      console.log('enrolling:', course_id)
      const response = await fetchUtil({
          endpoint: "enrollments",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"course_id": course_id, "user_id": this.user_id},
          user_id: this.user_id,
        });
        console.log(response);
        this.messages = response

        this.$router.push({ path: `course/${course_id}`});
      },
      async fetchCourseDetails(courseId) {
        try {
          const response = await fetchUtil({
            endpoint: `courses/${courseId}`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            user_id: this.user_id
          });
          this.course = response;
          console.log(this.course)
        } catch (error) {
          console.error("Error fetching course details:", error);
        }
      },
      enrollInCourse() {
        console.log("Enrolling in course:", this.course.id);
        this.addtocart(this.course.id, 1)
      },
      async checkCurrentUser(){
      const user_id = store.state.currentUser;
      
      if (user_id !== null) {
        const response2 = await fetchUtil({
            endpoint: `users/${user_id}`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            user_id: user_id
          });

        const user=response2
        
        // Check if this.user.courses exists and is an array
        if (Array.isArray(user.courses)) {
          // Iterate through each course and store course_id in user_enrolled
          for (const course of user.courses) {
            if (course.id) {
              this.user_enrolled.push(course.id);
            }
          }
        }

        // Optionally, you can log the user_enrolled array to verify
        console.log('User Enrolled',this.user_enrolled);
      } else {
        this.userLoggedIn = false;
      }
    }
    },
  };
  </script>