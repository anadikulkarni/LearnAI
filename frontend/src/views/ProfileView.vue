<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import store from '../store'
import fetchUtil from '../FetchUtil.js';
</script>

<template>
  <div class="bg-light py-3">
    <div class="container">
      <div class="row">
        <div class="col-md-12 mb-0">
          <RouterLink to="/">Home</RouterLink> 
          <span class="mx-2 mb-0">/</span> 
          <strong class="text-black">PROFILE</strong>
        </div>
      </div>
    </div>
  </div>

  <div v-if="userLoggedIn" class="site-section">
    <div class="container">
      <div class="row">
        <!-- Profile Information -->
        <div class="col-md-6">
          <div class="profile-container">
            <h6 class="text-primary text-uppercase text-center">Your Profile</h6>
            <form @submit.prevent="updateUserProfile">
              <div class="p-3 border">
                <div class="form-group">
                  <label for="username" class="text-black">Username</label>
                  <input type="text" class="form-control" id="username" v-model="user.username" readonly>
                </div>
                <div class="form-group">
                  <label for="role" class="text-black">Role</label>
                  <input type="text" class="form-control" id="role" v-model="user.roles[0].name" readonly>
                </div>
                <div class="form-group">
                  <label for="email" class="text-black">Email</label>
                  <input type="text" class="form-control" id="email" v-model="user.email" readonly>
                </div>
                <div class="form-group">
                  <label for="since" class="text-black">User Since</label>
                  <input type="text" class="form-control" id="since" v-model="user.created_at" readonly>
                </div>
                <div class="form-group text-center">
                  <button @click="signOut" type="button" class="btn btn-primary">Sign Out</button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Enrolled Courses -->
        <div class="col-md-6">
          <div class="courses-container">
            <h6 class="text-primary text-uppercase text-center">Enrolled Courses</h6>
            <div v-for="course in user.courses" :key="course.id" class="course-item p-3 border mb-3">
              <figure class="text-center">
                <RouterLink :to="'/course/' + course.id">
                  <img :src="'data:;base64,' + course.image" width="150" height="150" alt="Course Image" class="img-fluid">
                </RouterLink>
              </figure>
              <h3 class="text-center">
                <RouterLink :to="'/course/' + course.id">{{ course.title }}</RouterLink>
              </h3>
              <p>{{ course.description }}</p>
            </div>
            <div class="text-center">
              <RouterLink to="/learn">
                <button class="btn btn-primary">Go to Courses</button>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else>
    <div class="container text-center">
      <h3 class="text-danger mt-5">Please login to view and manage your profile!</h3>
      <RouterLink to="/login">
        <button type="button" class="btn btn-primary mt-3">Click here to login</button>
      </RouterLink>
    </div>
  </div>

  <FooterItem />
</template>

<script>
export default {
  data() {
    return {
      userLoggedIn: true, // Set this to the actual condition for user login
      user: null,
      addresses: null,
      newAddress: {
        address1: "",
        mobile: "",
      },
    };
  },
  beforeMount(){
    this.checkCurrentUser();
  },
  watch: {
    $route: 'checkCurrentUser',
    '$store.state.currentUser': 'checkCurrentUser',
  },
  methods: {
    updateUserProfile() {
      // Implement the logic to update user profile
    },
    async addAddress() {
      // Implement the logic to add a new address
      const user_id = store.state.currentUser
      console.log(user_id);
      const addr = this.newAddress.address1
      const mobile = this.newAddress.mobile
      const response = await fetchUtil({
          endpoint: "address",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"user_id": user_id, "address":addr, "mobile": mobile},
          user_id: user_id
        });
      console.log(response);
      location.reload();
    },
    signOut() {
      // Implement the logic to sign out the user
      const user_id = store.state.currentUser
      store.commit('clearUserData', {
      userId: user_id,
      });

      store.commit('clearUserTokens', {
      userId: user_id,
      });

      localStorage.clear();

      this.$router.push({ path: '/login' });
    },
    async checkCurrentUser(){
      const user_id = store.state.currentUser
      console.log("Profile Page: ", user_id)
      if(user_id !== null) {
        const response2 = await fetchUtil({
            endpoint: `users/${user_id}`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            user_id: user_id
          });
        // console.log(storedUserData)
        this.user = response2
        // console.log(this.user.username);
        // console.log(response);
      } else {
        this.userLoggedIn=false;
      }
    }
  },
};
</script>
<style scoped>
.profile-container, .courses-container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.course-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.course-item h3 {
  font-size: 1.25rem;
  margin-top: 10px;
}

.course-item p {
  font-size: 0.9rem;
  color: #6c757d;
  text-align: center;
}

@media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
</style>
  