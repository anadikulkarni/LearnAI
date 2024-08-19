<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
</script>


<template>
  <div class="site-wrap">
  
  <div class="bg-light py-3">
    <div class="container">
      <div class="row">
        <div class="col-md-12 mb-0"><a href="index.html">Home</a> <span class="mx-2 mb-0">/</span> <strong class="text-black">About</strong></div>
      </div>
    </div>
  </div>  

  <div class="site-section border-bottom">
    <div class="container">
      <div class="row justify-content-center mb-5">
        <div class="col-md-7 site-section-heading text-center pt-4">
          <h2>The Team</h2>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6 col-lg-3">

          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/me.png" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Azfar Faheem Mustafa</h3>
                <p class="block-38-subheading">21f2000478</p>
              </div>
              <div class="block-38-body">
                <p>Full Stack Developer at Intelliob Technologies, B.Tech in Computer Science specializing in AI and Big Data.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/shamel.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Shamel Fahd Mustafa</h3>
                <p class="block-38-subheading">21f1001139</p>
              </div>
              <div class="block-38-body">
                <p>Management Trainee : Operations at Dyooti,  BSc Data Science and Programming, IIT Madras</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/john.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">John Joshi Alapatt</h3>
                <p class="block-38-subheading">21f1005544</p>
              </div>
              <div class="block-38-body">
                <p>A.I Engineer at Tardid Technologies, B.S in Data Science and Applications, IIT Madras</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/velan.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Velan Saravanan</h3>
                <p class="block-38-subheading">21f1001998</p>
              </div>
              <div class="block-38-body">
                <p>B.S in Data Science and Applications, IIT Madras</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/Azhar.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Azarudin Bihari</h3>
                <p class="block-38-subheading">21f3000828</p>
              </div>
              <div class="block-38-body">
                <p>Data Scientist at Silver Brain AI, B.S in Data Science and Applications, IIT Madras </p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/Anadi.png" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Anadi Kulkarni</h3>
                <p class="block-38-subheading">21f1000235</p>
              </div>
              <div class="block-38-body">
                <p>B.S in Data Science and Applications, IIT Madras </p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/sukesh.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Sukesh S</h3>
                <p class="block-38-subheading">21f1000609</p>
              </div>
              <div class="block-38-body">
                <p>B.S in Data Science and Applications, IIT Madras</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  <div class="site-section border-bottom">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-6">
          <div class="block-16">
            <figure>
              <img src="../assets/images/blog_1.jpg" alt="Image placeholder" class="img-fluid rounded">
              
            </figure>
          </div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-5">
          
          
          <div class="site-section-heading pt-3 mb-4">
            <h2 class="text-black">How We Started</h2>
          </div>
          <p>Our journey began with a vision: to make high-quality education accessible to everyone, no matter their location or background. We started as a small initiative with a passion for learning, and have since grown into a leading platform for online education.

          We believe that knowledge should be available to all, and that's why we offer a diverse range of courses and resources at affordable prices. Our platform features courses from various fields, designed to help you advance your skills and achieve your educational goals.
          </p>

          <p>We're excited to have you on board and look forward to supporting your learning goals!</p>

        </div>
      </div>
    </div>
  </div>

  <FooterItem />
</div>
</template>


<!-- <style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style> -->