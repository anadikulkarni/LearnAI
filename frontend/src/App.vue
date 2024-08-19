<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Request from './components/RequestItem.vue';
import Sidebar from './components/GenAISidebar.vue'
import translate_sidebar from './components/TranslatorSidebar.vue'
import store from './store.js';
import fetchUtil from './FetchUtil.js';
import { ref, onMounted } from 'vue';

const isSidebarExpanded = ref(true);
const isSidebar2Expanded = ref(true);
const sidebarRef = ref(null);
const sidebar2Ref = ref(null);

onMounted(() => {
  // Sync with the initial state of the sidebar from localStorage
  isSidebarExpanded.value = localStorage.getItem("is_expanded") === "true";
  isSidebar2Expanded.value = localStorage.getItem("is_t_expanded") === "true";
});

const toggleSidebar = () => {
  console.log("toggled");
  isSidebarExpanded.value = !isSidebarExpanded.value;
  localStorage.setItem("is_expanded", isSidebarExpanded.value);
  // Ensure the Sidebar component reacts accordingly
  // if (isSidebarExpanded.value) {
  //   sidebarRef.value.ToggleMenu();
  // } else {
  //   sidebarRef.value.ToggleMenu();
  // }
};

const toggleSidebar2 = () => {
  console.log("toggled Translate Sidebar");
  isSidebar2Expanded.value = !isSidebar2Expanded.value;
  localStorage.setItem("is_t_expanded", isSidebar2Expanded.value);
  // Ensure the Sidebar component reacts accordingly
  // if (isSidebarExpanded.value) {
  //   sidebarRef.value.ToggleMenu();
  // } else {
  //   sidebarRef.value.ToggleMenu();
  // }
};

</script>

<template>
<Sidebar :key="isSidebarExpanded" :is-expanded="isSidebarExpanded" ref="sidebarRef"/>
<translate_sidebar :key="isSidebar2Expanded" :is_t_expanded="isSidebar2Expanded" ref="sidebar2Ref"/>
<main :class="{ 'sidebar-expanded': isSidebarExpanded }">
<header class="site-navbar" role="banner">
  <div class="site-navbar-top">
    <div class="container">
      <div class="row align-items-center">

        <div class="col-6 col-md-4 order-2 order-md-1 site-search-icon text-left">
          <form v-if="showSearchBar" @submit.prevent="searchProducts" class="site-block-top-search">
          <input type="text" class="form-control border-0" v-model="searchKeyword" @keydown.enter.prevent="submitForm" placeholder="Search Courses..">
          <span class="icon icon-search2"></span>
          <input type="submit" hidden />
          </form>
          <span v-if="!showSearchBar" class="icon icon-arrow_back"><router-link to="/">Back</router-link></span>
          <!-- <button @click="checkCurrentUser">test button</button> -->
        </div>

        <div class="col-12 mb-3 mb-md-0 col-md-4 order-1 order-md-2 text-center">
          <div class="site-logo">
            <router-link to="/" class="js-logo-clone">Learn AI</router-link>
          </div>
        </div>
        <div class="col-6 col-md-4 order-3 order-md-3 text-right">
          <div class="site-top-icons">
            <ul>
              <li v-if="userLoggedIn">
                <p></p>
                <router-link to="/profile">{{ userData.username }}<span class="icon icon-person"></span></router-link>
              </li>
              <li v-else>
                <p></p>
                <router-link to="/login"><span class="icon icon-person"></span></router-link>
              </li>

              <li><button class="icon icon-superpowers" @click="toggleSidebar"></button></li>
              <li>
                <router-link to="/profile" class="site-cart">
                  <span class="icon icon-book"></span>
                  <span class="count">{{ cartItemCount }}</span>
                </router-link>
              </li>
              <li class="d-inline-block d-md-none ml-md-0"><a href="#" class="site-menu-toggle js-menu-toggle"><span class="icon-menu"></span></a></li>
            </ul>
          </div>
        </div>

      </div>
    </div>
  </div>
  <nav class="site-navigation text-right text-md-center" role="navigation">
    <div class="container">
      <ul class="site-menu js-clone-nav d-none d-md-block">

        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/learn">Learn</router-link></li>
        <li v-if="showSearchBar" class="has-children">
          <router-link to="/learn">Browse by Category</router-link>
          <ul class="dropdown">
            <li v-for="category in categories" :key="category.id">
              <router-link :to="'/learnbycategory?category_id=' + category.id">{{ category.name }}</router-link>
            </li>
          </ul>
        </li>
        <li><router-link to="/about">About</router-link></li>
        <!-- <li><router-link to="/admin">Admin Panel</router-link></li> -->
        <li v-if="isAdmin"><router-link to="/admin">Admin Panel</router-link></li>
      </ul>
    </div>
  </nav>
</header>
</main>
    <Request
      endpoint="categories"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleCats"
    />

  <RouterView />

  <div class="floating-button-container">
    <button class="floating-button" @click="toggleSidebar">
      <span class="icon icon-superpowers"></span>
    </button>
  </div>

  <div class="floating-button-container">
    <button class="floating-button2" @click="toggleSidebar2">
      <span class="icon icon-language"></span>
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showSearchBar: true,
      searchKeyword: '', // search keyword data property
      userLoggedIn: false, // user login status data property
      userData: null,
      cartItemCount: 0, // Sample cart item count data property
      categories: [],
      products: [],
      isAdmin: null ,// admin status data property
    };
  },
  mounted() {
    this.checkCurrentRoute();
  },

  watch: {
    $route: {
    handler: 'handleRouteChange',
    immediate: true, // Run the handler immediately when the component is created
    },
    '$store.state.currentUser': 'checkCurrentUser',
  },
  methods: {
    handleRouteChange() {
    this.checkCurrentRoute();
    this.checkCurrentUser();
    // Add any additional logic you need when $route changes
    },
    submitForm() {
      this.$router.push({ path: '/learnbycategory', query: { keyword: this.searchKeyword } });
    },
    searchProducts() {
      console.log('Searching for courses with keyword:', this.searchKeyword);
      this.submitForm();
    },
    checkCurrentRoute() {
      // Check if the current route is /shopbycategory
      this.showSearchBar = this.$route.path !== '/learnbycategory';
    },
    handleCats(responseData) {
      // Handle the response data here
      this.categories=responseData;
      console.log(responseData);
    },
    async getCartLength(){
      const user_id = store.state.currentUser
      const response = await fetchUtil({
          endpoint: `enrollments/${user_id}`,
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: user_id
        });
        this.cartItemCount = response.enrolled_courses.length
        console.log("length:", this.cartItemCount);
    },
    checkCurrentUser(){
      const user_id = store.state.currentUser
      console.log("Home Page: ", user_id)
      if(user_id !== null) {
        const storedUserData = store.state.users[user_id].userData
        console.log(user_id)
        this.userData = storedUserData
       // Check if any Admin, Creator or Instructor
        const hasAdminRole = this.userData.roles.some(role => [1, 2, 4].includes(role.id));
        this.isAdmin = hasAdminRole;
        this.userLoggedIn=true
        this.getCartLength();
        // console.log(this.userData.firstname);
        console.log(this.isAdmin);
      } 
    }
  },
  components: {
    Request,
  },
};
</script>
<style scoped>
#app {
  display: flex;
}

.floating-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.floating-button2 {
  position: fixed;
  bottom: 20px;
  right: 125px;
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.floating-button:hover {
  background-color: #0056b3;
}

.floating-button:focus {
  outline: none;
}

main {
  flex: 1;
  transition: margin-left 0.2s ease-in-out;

  &.sidebar-expanded {
    margin-left: var(--sidebar-width); /* Adjust this variable as needed */
  }

  @media (max-width: 1024px) {
    margin-left: 0;
  }
}
</style>


/* <!-- <style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> --> */
