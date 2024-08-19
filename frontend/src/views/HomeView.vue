<script setup>
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
import Sidebar from '../components/GenAISidebar.vue'
import { ref, onMounted } from 'vue';

const isSidebarExpanded = ref(true);
const sidebarRef = ref(null);

onMounted(() => {
  // Sync with the initial state of the sidebar from localStorage
  isSidebarExpanded.value = localStorage.getItem("is_expanded") === "true";
});

const toggleSidebar = () => {
  console.log("toggled");
  isSidebarExpanded.value = !isSidebarExpanded.value;
  localStorage.setItem("is_expanded", isSidebarExpanded.value);
  // Ensure the Sidebar component reacts accordingly
  if (isSidebarExpanded.value) {
    sidebarRef.value.ToggleMenu();
  } else {
    sidebarRef.value.ToggleMenu();
  }
};

</script>

<template>
  <Sidebar :key="isSidebarExpanded" :is-expanded="isSidebarExpanded" ref="sidebarRef"/>
  <main>
    <div class="site-wrap">
<div style="
    background-image: url('https://i.postimg.cc/V63jCH9F/pexels-pavel-danilyuk-8294657.jpg');
    height: 400px;"
    class="site-blocks-cover">
  <div class="container">
    <div class="row align-items-start align-items-md-center justify-content-end">
      <div class="col-md-5 text-center text-md-left pt-5 pt-md-0">
        <h1 class="mb-2 text-white">Unlock Your Learning Potential!</h1>
        <div class="intro-text text-center text-md-left">
          <p class="mb-4 text-white">Welcome to Learn AI! We're here to make your educational journey as seamless and engaging as possible.</p>
          <p>
            <router-link v-if="userLoggedIn" to="/learn" class="btn btn-primary">Learn Now</router-link>
            <router-link v-else to="/learn" class="btn btn-primary" style="margin-right: 10px">Learn Now</router-link>
            <button @click="toggleSidebar" class="btn btn-primary" style="margin-right: 10px">Summon the AI</button>

            <!-- <router-link v-else to="/login" class="btn btn-primary" style="margin-right: 10px">Sign in</router-link>
            <router-link v-else to="/register" class="btn btn-primary">Sign Up</router-link> -->
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

  <div class="site-section site-section-sm site-blocks-1">
    <div class="container">
      <div class="row">
        <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
          <div class="icon mr-4 align-self-start">
            <span class="icon-book"></span>
          </div>
        <div class="text">
    <h2 class="text-uppercase">Personalized Learning</h2>
    <p>Experience tailored courses and resources that adapt to your learning style and pace, ensuring you achieve your educational goals efficiently.</p>
  </div>
  </div>
  <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
    <div class="icon mr-4 align-self-start">
      <span class="icon-road"></span>
    </div>
    <div class="text">
      <h2 class="text-uppercase">Flexible Learning Paths</h2>
      <p>Whether you're advancing your career or expanding your knowledge, our flexible course structures allow you to learn at your own pace, on your own schedule.</p>
    </div>
  </div>
  <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
    <div class="icon mr-4 align-self-start">
      <span class="icon-phone"></span>
    </div>
    <div class="text">
      <h2 class="text-uppercase">24/7 Support</h2>
      <p>Our support team is available around the clock to assist you with any questions or challenges you encounter during your learning journey.</p>
    </div>
  </div>

    </div>
  </div>
</div>

<div class="site-section block-3 site-blocks-2 bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-7 site-section-heading text-center pt-4">
          <h2>Featured Courses</h2>
        </div>
      </div>
  <br>
  <div class="container">
  <div class="row">
    <div
      v-for="(course, i) in courses.slice(0, 3)"
      :key="course.id"
      class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-6 nonloop-block-3 owl-carousel"
    >
      <figure>
        <router-link :to="'/shopsingle?id=' + course.id">
          <!-- Add an image if available in the course object, otherwise, leave it commented -->
          <img :src="course.image ? 'data:image/jpeg;base64,' + course.image : 'default-image.jpg'" width="150" height="150" alt="Course Image" class="img-fluid">
          <!-- <img src="../assets/images/store.jpg" width="150" height="150" alt="Course Image" class="img-fluid"> -->
        </router-link>
      </figure>
      <div class="block-4-text p-4">
        <h3>
          <router-link :to="'/shopsingle?course_id=' + course.id">{{ course.title }}</router-link>
        </h3>
        <p class="mb-0">{{ course.description }}</p>
        <p class="text-primary font-weight-bold">
          {{ course.ratings.length > 0 ? course.ratings[0].rating + ' stars' : 'No ratings yet' }}
        </p>
      </div>
    </div>
  </div>
</div>
    </div>
  </div>

<div class="site-section block-8">
  <div class="container">
    <div class="row justify-content-center  mb-5">
      <div class="col-md-7 site-section-heading text-center pt-4">
        <h2>Start Learning Now!</h2>
      </div>
    </div>
    <div class="row align-items-center">
      <div class="col-md-12 col-lg-7 mb-5">
        <a href="#"><img src="../assets/images/blog_1.jpg" alt="Image placeholder" class="img-fluid rounded"></a>
      </div>
      <div class="col-md-12 col-lg-5 text-center pl-md-5">
        <h2><a href="#">ENROLL NOW & SAVE 20%</a></h2>
        <h5><a href="#">Use code LEARN20 at checkout</a></h5>
        <p class="post-meta mb-4"><span class="block-8-sep">&bullet;</span>Valid for new course enrollments only.</p>
        <p>Get a 20% discount on your first course enrollment using code LEARN20. Don’t miss out on this opportunity to expand your knowledge and skills!</p>
        <p><a href="#" class="btn btn-primary">Browse Courses</a></p>
      </div>
    </div>
  </div>
</div>

</div>
    <FooterItem />
    <Request
      endpoint="courses"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleCourses"
    />
  </main>
</template>

<script>
export default {
  data() {
    return {
      userLoggedIn: false, // Replace with your actual user login status
      imageurl: '../assets/images/hero.jpg',
      imageurl2: '../assets/images/store.jpg',
      courses: [],
      // ... Add other data properties as needed
    };
  },
  components: {
    Request,
    FooterItem,
  },
  methods: {
    handleCourses(responseData) {
      // Handle the response data here
      this.courses=responseData;
      console.log(responseData);
    },
    getRandomInt(max) {
      return Math.floor(Math.random() * max);
    },
  }
  // ... Add methods, computed properties, etc., as needed
};
</script>