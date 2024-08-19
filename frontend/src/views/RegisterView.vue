<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import store from '../store'
import fetchUtil from '../FetchUtil.js';
</script>

<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">REGISTER</strong></div>
        </div>
      </div>
    </div>

    <div class="site-section">
      <div class="container" style="align: center;">
        <div class="row">
          <div class="col-md-12"></div>
          <div class="col-md-6">
            <form @submit.prevent="signUpUser">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="username" class="text-black">username<span class="text-danger">*</span></label>
                    <input v-model="username" type="text" class="form-control" id="username" name="username" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="email" class="text-black">Email<span class="text-danger">*</span></label>
                    <input v-model="email" type="text" class="form-control" id="email" name="email" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="password" class="text-black">Password<span class="text-danger">*</span></label>
                    <input v-model="password" type="password" class="form-control" id="password" name="password" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="password2" class="text-black">Repeat Password<span class="text-danger">*</span></label>
                    <input v-model="password2" type="password" class="form-control" id="password2" name="password2" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="role" class="text-black">Select your Role<span class="text-danger">*</span></label>
                    <select v-model="role" class="form-control" id="role" name="role" required>
                      <option value="2">Creator</option>
                      <option value="4">Teacher/Instructor</option>
                      <option value="5">Student</option>
                    </select>
                  </div>
                </div>

              <!-- Additional field for employee ID (conditionally rendered) -->
              <div v-if="role !== '5' && role !== null" class="form-group row">
                <div class="col-md-12">
                  <label for="employeeId" class="text-black">Employee ID (for verification)<span class="text-danger">*</span></label>
                  <input
                    v-model="employeeId"
                    type="text"
                    class="form-control"
                    id="employeeId"
                    name="employeeId"
                    required
                  />
                  <label for="employeeId" class="text-black"><span class="text-danger">Please note that until approval by Admin, your account will not gain access to insrtuctor/creator panel.</span></label>
                </div>
              </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <button type="submit" class="btn btn-primary btn-lg btn-block">Sign Up</button>
                  </div>
                  <router-link to="/login" style="margin-left: auto; margin-right: auto; margin-top:20px;"><button type="button" class="btn btn-link btn-sm">Already a User? Log in Now!</button></router-link>
                </div>
              </div>
            </form>
          </div>

          <div class="col-md-5 ml-auto">
            <div class="p-4 border mb-3">
              <span class="d-block text-primary h6 text-uppercase" style="text-align: center;">Welcome to Learn AI</span>
              <img src="../assets/images/learnbanner.png" class="img-thumbnail" alt="Grocery store">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <FooterItem />
</template>

<script>
export default {
  data() {
    return {
      isStoreManager: false,
      employeeId: '',
      username: '',
      email: '',
      password: '',
      password2: '',
      role: null,
    };
  },
  methods: {
    async signUpUser() {
      const response = await fetchUtil({
          endpoint: "signup",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"username": this.username, "password1": this.password, "password2": this.password2, "email": this.email, "role_id": this.role, "employee_id": this.employeeId},
        });
      console.log(response);
      this.$router.push({ path: '/login', query: { message: response.message } });
    },
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
  