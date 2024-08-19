<script setup>
import { RouterLink, RouterView } from 'vue-router'
import store from '../store'
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
import fetchUtil from '../FetchUtil.js';
</script>

<template>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">Learn</strong></div>
        </div>
      </div>
    </div>

    <div class="site-section">
  <div class="container">

    <div class="row mb-5">
      <div class="col-md-9 order-2">

        <div class="row">
          <div class="col-md-12 mb-5">
            <div class="float-md-center mb-4"><h2 class="text-black h5">
              <!-- Vue.js messages placeholder -->
            </h2></div>
            <div class="float-md-left mb-4"><h2 class="text-black h5">{{ shoptitle }}</h2></div>
            <div class="d-flex">
              <div class="btn-group mr-1 ml-md-auto">
                <button type="button" class="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuReference" data-toggle="dropdown">CATEGORIES</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuReference">
                  <a class="dropdown-item" href="/learn">All</a>
                  <!-- Vue.js categories loop placeholder -->
                </div>
              </div>
              <div class="btn-group">
                <button type="button" class="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuReference" data-toggle="dropdown">SORT BY</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuReference">
                  <a class="dropdown-item" href="#">Relevance</a>
                  <a class="dropdown-item" href="#">Name, A to Z</a>
                  <a class="dropdown-item" href="#">Name, Z to A</a>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">Price, low to high</a>
                  <a class="dropdown-item" href="#">Price, high to low</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row mb-5">
          <!-- Vue.js courses loop placeholder -->
          <!-- Each course should have its own Vue.js form -->
          <div v-for="course in courses" :key="course.id" class="col-sm-6 col-lg-4 mb-4">
            <div class="block-4 text-center border">
              <div :id="course.id" :name="course.id">
                <figure class="block-4-image">
                  <router-link :to="'/course/' + course.id">
                    <img :src="'data:;base64,' + course.image" width="150" height="150" alt="course Image" class="img-fluid">
                  </router-link>
                </figure>
                <div class="block-4-text p-4">
                  <h3><router-link :to="'/course/' + course.id">{{ course.title }}</router-link></h3>
                  <p class="mb-0">{{ course.description }}</p>
                  <!-- <p class="text-primary font-weight-bold">Ratings: {{ course.ratings.length > 0 ? course.ratings[0].rating : 'No ratings yet' }} <span class="icon-star"></span></p> -->
                  <!-- Vue.js stock and quantity logic placeholder -->
                  <p class="text-primary">Instructor Contact</p>
                  <p class="text-primary font-weight-bold">{{ course.instructor.email }}</p>
                  
                  <div class="icon mr-4 align-self-start">
                    <p><span class="icon-play icon mr-4 align-self-start"></span>{{ course.videos.length }} Lectures </p>
                  </div>
                  <div class="text">
                    
                </div>
                </div>
                <div v-if="userLoggedIn" class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                <p></p>
                <button 
                  @click="enroll(course.id)" 
                  :class="user_enrolled.includes(course.id) ? 'btn btn-secondary' : 'btn btn-primary'" 
                  :disabled="user_enrolled.includes(course.id)">
                  {{ user_enrolled.includes(course.id) ? 'ENROLLED' : 'ENROLL' }}
                </button>
                </div>
                <div v-else class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                <p></p>
                <button @click="altenroll" class="btn btn-primary">ENROLL</button>
                </div>
              </div>
            </div>
          </div>
          <!-- End Vue.js courses loop placeholder -->
        </div>
        <div v-if="courses.length === 0" class="float-md-left mb-4"><h2 class="text-danger h5">No Results found!</h2></div>
      </div>

      <div class="col-md-3 order-1 mb-5 mb-md-0">
        <div class="border p-4 rounded mb-4">
          <h3 class="mb-3 h6 text-uppercase text-black d-block">Categories</h3>
          <ul class="list-unstyled mb-0">
            <li class="mb-1"><router-link to="/learn" class="d-flex"><span>View All</span> <span class="text-black ml-auto"></span></router-link></li>
            <li v-for="category in cats" :key="category.id" class="mb-1">
              <router-link :to="'/learnbycategory?category_id=' + category.id" class="d-flex">
                <span>{{ category.name }}</span>
                <span class="text-black ml-auto"></span>
              </router-link>
            </li>
          </ul>
        </div>
        <ul class="list-unstyled mb-0" v-if="messages.length > 0">
            <h5 v-for="(message, index) in messages" :key="index" class="text-success">{{ message }}</h5>
        </ul>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12">
        <div class="site-section site-blocks-2">
          <div class="row justify-content-center text-center mb-5">
            <!-- Pagination or additional content goes here -->
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
      <Request
      endpoint="courses"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleCourses"
    />

    <Request
      endpoint="categories"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleCats"
    />

    <FooterItem />
  </template>

<script>
export default {
  data() {
    return {
      messages: [],
      shoptitle: "Course Catalogue",
      courses: [],
      user_id: store.state.currentUser,
      cats: [],
      userLoggedIn: true,
      user_enrolled: []
    };
  },
  mounted() {
    // Add any additional logic that should run after the component is mounted
  },
  components: {
    Request,
    FooterItem,
  },
  beforeMount(){
    this.checkCurrentUser();
  },
  // watch: {
  //   $route: 'checkCurrentUser',
  //   '$store.state.currentUser': 'checkCurrentUser',
  // },
  methods: {
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
    altenroll(){
      this.$router.push({ path: '/login', query: { message: "Please login to start enrolling!" } });
      // this.$router.push({ path: `course/${this.courses[0].id}`});
    },
    // handlecourses(responseData) {
    //   // Handle the response data here
    //   // this.courses=responseData;
    //   this.courses = responseData.map(course => ({ ...course, qty: 1 }));
    //   console.log(responseData);
    // },
    handleCourses(responseData) {
      // Handle the response data here
      this.courses=responseData;
      console.log(responseData);
    },
    handleCats(responseData) {
      // Handle the response data here
      this.cats=responseData;
      console.log(responseData);
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

  
  <style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
  </style>
  