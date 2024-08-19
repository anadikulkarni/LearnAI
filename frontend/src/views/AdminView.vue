<template>
  <div>
    <!-- Admin Panel Header -->
    <div class="bg-light py-3">
      <div class="container" v-if="isadmin">
        <div class="row">
          <div class="col-md-12 mb-0">
            <router-link to="/">Home</router-link>
            <span class="mx-2 mb-0">/</span>
            <strong class="text-black">Admin Panel</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- Admin Panel Content -->
    <div v-if="isadmin" class="site-section">
      <div class="container">

        <!-- Manager Access Approval Section -->
        <!-- <div class="row mb-5">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Teacher/Instructor Access Approval</h2>
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th class="product-name">Employee ID</th>
                  <th class="product-thumbnail">Full Name</th>
                  <th class="product-name">Email</th>
                  <th class="product-name">Mobile Number</th>
                  <th class="product-price">Status</th>
                  <th class="product-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="approval in mgrapprovals" :key="approval.user_id">
                  <td class="product-name">
                    <strong>{{ approval.employee_id }}</strong>
                  </td>
                  <td class="product-name">
                    <strong>{{ approval.firstname }} {{ approval.lastname }}</strong>
                  </td>
                  <td class="product-name">
                    <strong>{{ approval.email }}</strong>
                  </td>
                  <td class="product-name">
                    <strong>{{ approval.mobile }}</strong>
                  </td>
                  <td class="product-name">
                    <strong>{{ approval.status }}</strong>
                  </td>
                  <td class="product-actions">
                    <button @click="handleMgrApproval(approval.user_id, 0)" class="btn btn-danger btn-sm">
                      <span class="icon icon-delete"></span>
                    </button>
                    <button @click="handleMgrApproval(approval.user_id, 1)" class="btn btn-success btn-sm" style="margin-right:10px;">
                      <span class="icon icon-check"></span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div> -->

        <!-- Category Management Section -->
        <div class="row mb-5">
          <div class="col-md-7">
            <form @submit.prevent="addCategory" method="post">
              <h2 class="h3 mb-3 text-black">Add Category</h2>
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <ul class="flashes" v-if="catmessages.length > 0">
                    <li v-for="(message, index) in catmessages" :key="index" class="text-success">{{ message }}</li>
                  </ul>

                  <div class="col-md-12">
                    <label for="name" class="text-black">Category name <span class="text-danger">*</span></label>
                    <input v-model="newCategory.name" type="text" class="form-control" id="name" name="name" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Category">
                  </div>
                </div>
              </div>
            </form>
          </div>

          <div class="col-md-5 ml-auto">
            <h2 class="h3 mb-3 text-black">Category List</h2>
            <div class="col-md-18">
              <ul class="flashes" v-if="catmessages2.length > 0">
                <li v-for="(message, index) in catmessages2" :key="index" class="text-success">{{ message }}</li>
              </ul>
              <div v-for="category in categories" :key="category.category_id">
                <div v-if="category.editMode">
                  <form @submit.prevent="saveCategory(category)">
                    <input v-model="category.name" class="form-control" />
                    <button type="submit" class="btn btn-success btn-sm">Save</button>
                    <button @click="cancelEdit(category)" class="btn btn-secondary btn-sm">Cancel</button>
                  </form>
                </div>
                <div v-else>
                  <div class="p-1 p-lg-1 border">
                    {{ category.name }}
                    <button @click="editCategory(category)" class="btn btn-primary btn-sm" style="float:right;">
                      <span class="icon icon-edit"></span>
                    </button>
                    <button @click="confirmDeletecat(category.id, category.name)" class="btn btn-danger btn-sm" style="float:right; margin-right:10px;">
                      <span class="icon icon-delete"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Course Management Section -->
        <div class="row mb-5">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Manage Courses</h2>

            <!-- Form to Add New Course -->
            <form @submit.prevent="addCourse" method="post">
              <h2 class="h3 mb-3 text-black">Add Course</h2>
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <ul class="flashes" v-if="courseMessages.length > 0">
                    <li v-for="(message, index) in courseMessages" :key="index" class="text-success">{{ message }}</li>
                  </ul>

                  <div class="col-md-12">
                    <label for="title" class="text-black">Course Title <span class="text-danger">*</span></label>
                    <input v-model="newCourse.title" type="text" class="form-control" id="title" name="title" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="description" class="text-black">Course Description <span class="text-danger">*</span></label>
                    <textarea v-model="newCourse.description" class="form-control" id="description" name="description" required></textarea>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="category" class="text-black">Category<span class="text-danger">*</span></label>
                    <select v-model="newCourse.category_id" name="category_id" id="category_id" class="form-control">
                      <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="instructor" class="text-black">Instructor<span class="text-danger">*</span></label>
                    <select v-model="newCourse.instructor_id" name="instructor_id" id="instructor_id" class="form-control">
                      <option v-for="instructor in instructors" :key="instructor.id" :value="instructor.id">
                        {{ instructor.username }} - {{ instructor.email }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="youtube_playlist" class="text-black">YouTube Playlist URL</label>
                    <input v-model="newCourse.youtube_playlist" type="url" class="form-control" id="youtube_playlist" name="youtube_playlist">
                  </div>
                </div>
                <div class="form-group row">
                <div class="col-md-12">
                  <label for="image" class="text-black">Course Display Image</label><span class="text-danger">*</span>
                  <input accept=".jpg, .jpeg, .png, .gif" @change="onFileChange" type="file" name="image" class="form-control" id="image" required>
                </div>
              </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Course">
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Display Existing Courses -->
        <div class="row">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Course List</h2>
            <ul class="flashes" v-if="course2Messages.length > 0">
                    <li v-for="(message, index) in course2Messages" :key="index" class="text-success">{{ message }}</li>
            </ul>
            <div v-for="course in courses" :key="course.id">
              <div v-if="course.editMode">
                <form @submit.prevent="saveCourse(course)">
                  <input v-model="course.title" class="form-control" placeholder="Title"/>
                  <textarea v-model="course.description" class="form-control" placeholder="Description"></textarea>
                  <input v-model="course.category_id" type="number" class="form-control" placeholder="Category ID"/>
                  <input v-model="course.instructor_id" type="number" class="form-control" placeholder="Instructor ID"/>
                  <input v-model="course.youtube_playlist" type="url" class="form-control" placeholder="YouTube Playlist URL"/>
                  <button type="submit" class="btn btn-success btn-sm">Save</button>
                  <button @click="cancelCourseEdit(course)" class="btn btn-secondary btn-sm">Cancel</button>
                </form>
              </div>
              <div v-else>
                <div class="course-card">
                  <figure class="course-image">
                    <router-link :to="'/course/' + course.id">
                      <img :src="'data:;base64,' + course.image" alt="course Image" class="img-fluid">
                    </router-link>
                  </figure>
                  <div class="course-content">
                    <router-link :to="'/course/' + course.id">{{ course.title }} - {{ course.description }}</router-link>
                    <button @click="confirmDeleteCourse(course.id, course.title)" class="btn btn-danger btn-sm">
                      <span class="icon icon-delete"></span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Assignment Section -->
         <br>
         <br>
        <div class="row mb-5">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Add Assignment</h2>
            <ul class="flashes" v-if="assignmentMessages.length > 0">
                    <li v-for="(message, index) in assignmentMessages" :key="index" class="text-success">{{ message }}</li>
            </ul>
            <!-- Form to Add New Assignment -->
            <form @submit.prevent="addAssignment" method="post">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="course" class="text-black">Select Course <span class="text-danger">*</span></label>
                    <select v-model="newAssignment.course_id" name="course_id" id="course_id" class="form-control" required>
                      <option v-for="course in courses" :key="course.id" :value="course.id">
                        {{ course.title }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="title" class="text-black">Assignment Title <span class="text-danger">*</span></label>
                    <input v-model="newAssignment.title" type="text" class="form-control" id="title" name="title" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="description" class="text-black">Assignment Description <span class="text-danger">*</span></label>
                    <textarea v-model="newAssignment.description" class="form-control" id="description" name="description" required></textarea>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Assignment">
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Add Resources Section -->
        <div class="row mb-5">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Add Resources</h2>
            <ul class="flashes" v-if="resourceMessages.length > 0">
                    <li v-for="(message, index) in resourceMessages" :key="index" class="text-success">{{ message }}</li>
            </ul>
            <!-- Form to Add New Resource -->
            <form @submit.prevent="addResource" method="post">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="course" class="text-black">Select Course <span class="text-danger">*</span></label>
                    <select v-model="newResource.course_id" name="course_id" id="course_id" class="form-control" required>
                      <option v-for="course in courses" :key="course.id" :value="course.id">
                        {{ course.title }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="url" class="text-black">Resource URL <span class="text-danger">*</span></label>
                    <input v-model="newResource.url" type="url" class="form-control" id="url" name="url" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Resource">
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- Add Lab Assignment Section -->
        <div class="row mb-5">
          <div class="col-md-12">
            <h2 class="h3 mb-3 text-black">Add Lab Assignment</h2>
            <ul class="flashes" v-if="labMessages.length > 0">
                    <li v-for="(message, index) in labMessages" :key="index" class="text-success">{{ message }}</li>
            </ul>
            <!-- Form to Add New Lab Assignment -->
            <form @submit.prevent="addLabAssignment" method="post">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="course" class="text-black">Select Course <span class="text-danger">*</span></label>
                    <select v-model="newLabAssignment.course_id" name="course_id" id="course_id" class="form-control" required>
                      <option v-for="course in courses" :key="course.id" :value="course.id">
                        {{ course.title }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="title" class="text-black">Lab Assignment Title <span class="text-danger">*</span></label>
                    <input v-model="newLabAssignment.title" type="text" class="form-control" id="title" name="title" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="description" class="text-black">Description<span class="text-danger">*</span></label>
                    <input v-model="newLabAssignment.description" type="text" class="form-control" id="description" name="description" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="ex_input" class="text-black">Example Input <span class="text-danger">*</span></label>
                    <textarea v-model="newLabAssignment.ex_input" class="form-control" id="ex_input" name="ex_input" required></textarea>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="ex_output" class="text-black">Example Output <span class="text-danger">*</span></label>
                    <textarea v-model="newLabAssignment.ex_output" class="form-control" id="ex_output" name="ex_output" required></textarea>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Lab Assignment">
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>


      </div>
    </div>

    <div v-if="!isadmin" class="site-section">
      <div class="container">
        <h1 class="h3 mb-3 text-danger"><strong>Unauthorized Access, only Admins can access this page.</strong></h1>
      </div>
    </div>
    

    <FooterItem />
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import fetchUtil from '../FetchUtil.js';
import axios from 'axios';
import store from '../store.js';

export default {
  data() {
    return {
      isadmin: false,
      mgrapprovals: [],
      newCategory: {
        "name": ""
      },
      categories: [],
      catmessages: [],
      catmessages2: [],
      newCourse: {
        "title": "",
        "description": "",
        "category_id": "",
        "instructor_id": "",
        "youtube_playlist": "",
        "image": "",
      },
      newAssignment: {
        "course_id": "",     
        "title": "",      
        "description": "",  
      },
      newResource: {
        "course_id": "",       
        "url": "",
      },
      newLabAssignment: {
        "course_id": "",
        "description": "",
        "title": "",   
        "ex_input": "",
        "ex_output": "",  
      },
      courses: [],
      courseMessages: [],
      course2Messages: [],
      assignmentMessages: [],
      resourceMessages: [],
      labMessages: [],
      instructors: [],
    };
  },
  mounted() {
    this.checkAdmin();
    // this.loadManagerApprovals();
    this.loadCategories();
    this.loadCourses();
  },
  components: {
    RouterLink,
    FooterItem,
  },
  methods: {
    onFileChange(event) {
      const reader = new FileReader();
      // console.log(event.target.files[0]);
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (e) => {
      // Update the imageData with the base64 representation of the image
      const imageData = e.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, '');
      // console.log(imageData)
      this.newCourse.image=imageData.toString()
      };
    },
    checkAdmin() {
      const user_id = store.state.currentUser
      const storedUserData = store.state.users[user_id].userData
      console.log(user_id)
      this.userData = storedUserData
      const hasAdminRole = this.userData.roles.some(role => [1, 2, 4].includes(role.id));
      this.isadmin = hasAdminRole;
    },
    async loadManagerApprovals() {
      try {
        const response = await fetchUtil({
          endpoint: 'manager-approvals',
          method: 'GET',
        });
        this.mgrapprovals = response;
      } catch (error) {
        console.error('Error loading manager approvals:', error);
      }
    },
    handleMgrApproval(userId, status) {
      fetchUtil({
        endpoint: `manager-approval/${userId}`,
        method: 'PUT',
        data: { status },
      })
        .then(() => this.loadManagerApprovals())
        .catch(error => console.error('Error updating manager approval:', error));
    },
    async loadCategories() {
      try {
        const response = await fetchUtil({
          endpoint: 'categories',
          method: 'GET',
        });
        this.categories = response;

        const response2 = await fetchUtil({
          endpoint: 'users',
          method: 'GET',
        });
        this.instructors = response2;
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    },
    async addCategory() {
      if (!this.newCategory.name) {
        alert('Category name is required!');
        return;
      }

      try {
        console.log(this.newCategory);
        const response = await fetchUtil({
          endpoint: 'categories',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          data: this.newCategory,
        });
        this.catmessages.push(`Category "${this.newCategory.name}" added successfully!`);
        this.loadCategories(); // Reload categories after adding
        this.newCategory.name = ''; // Clear the input field
      } catch (error) {
        console.error('Error adding category:', error);
        alert('Error adding category');
      }
    },
    editCategory(category) {
      category.editMode = true;
    },
    async saveCategory(category) {
      try {
        await fetchUtil({
          endpoint: `categories/${category.id}`,
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          data: { name: category.name },
        });
        this.catmessages2.push(`Category "${category.name}" updated successfully!`);
        category.editMode = false;
      } catch (error) {
        console.error('Error updating category:', error);
      }
    },
    cancelEdit(category) {
      category.editMode = false;
    },
    async confirmDeletecat(category_id, name) {
      if (confirm(`Are you sure you want to delete category "${name}"?`)) {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/categories/${category_id}`);
          this.loadCategories(); // Reload categories after deletion
          this.catmessages2.push(`Category "${name}" deleted successfully!`);
        } catch (error) {
          console.error('Error deleting category:', error);
        }
      }
    },

    async loadCourses() {
      try {
        const response = await fetchUtil({
          endpoint: 'courses',
          method: 'GET',
        });
        this.courses = response;
      } catch (error) {
        console.error('Error loading courses:', error);
      }
    },
    async addCourse() {
      if (!this.newCourse.title || !this.newCourse.description || !this.newCourse.category_id || !this.newCourse.instructor_id) {
        alert('All fields are required!');
        return;
      }

      try {
        this.newCourse.category_id = String(this.newCourse.category_id);
        this.newCourse.instructor_id = String(this.newCourse.instructor_id);

        console.log(JSON.stringify(this.newCourse));

        const response = await axios.post('http://127.0.0.1:5000/api/courses', this.newCourse, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        this.courseMessages.push(`Course "${this.newCourse.title}" added successfully!`);
        this.loadCourses(); // Reload courses
        this.newCourse = { title: '', description: '', category_id: '', instructor_id: '', youtube_playlist: '', image: '' }; // Clear the form
      } catch (error) {
        console.error('Error adding course:', error);
        alert('Error adding course');
      }
    },
    editCourse(course) {
      course.editMode = true;
    },
    async saveCourse(course) {
      try {
        await fetchUtil({
          endpoint: `courses/${course.id}`,
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          data: {
            title: course.title,
            description: course.description,
            category_id: course.category_id,
            instructor_id: course.instructor_id,
            youtube_playlist: course.youtube_playlist
          },
        });
        this.course2Messages.push(`Course "${course.title}" updated successfully!`);
        course.editMode = false;
      } catch (error) {
        console.error('Error updating course:', error);
      }
    },
    cancelCourseEdit(course) {
      course.editMode = false;
    },
    async confirmDeleteCourse(course_id, title) {
      if (confirm(`Are you sure you want to delete course "${title}"?`)) {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/courses/${course_id}`);
          this.course2Messages.push(`Course "${title}" deleted successfully!`);
          this.loadCourses(); // Reload courses after deletion
        } catch (error) {
          console.error('Error deleting course:', error);
        }
      }
    },

    async addAssignment() {
      if (!this.newAssignment.course_id || !this.newAssignment.title || !this.newAssignment.description) {
        alert('Course, title, and description are required!');
        return;
      }

      try {
        console.log(this.newAssignment);
        const response = await axios.post('http://127.0.0.1:5000/api/assignments', this.newAssignment, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.assignmentMessages.push(`Assignment "${this.newAssignment.title}" added successfully!`);
        // this.loadAssignments(); // Reload assignments after adding
        this.newAssignment = {
          course_id: '',
          title: '',
          description: '',
        }; // Clear the input fields
      } catch (error) {
        console.error('Error adding assignment:', error);
        alert('Error adding assignment');
      }
    },

    async addResource() {
      if (!this.newResource.course_id || !this.newResource.url) {
        alert('Course and resource URL are required!');
        return;
      }

      try {
        console.log(this.newResource);
        const response = await axios.post('http://127.0.0.1:5000/api/resources', this.newResource, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.resourceMessages.push('Resource added successfully!');
        // this.loadResources(); // Reload resources after adding
        this.newResource = {
          course_id: '',
          url: '',
        }; // Clear the input fields
      } catch (error) {
        console.error('Error adding resource:', error);
        alert('Error adding resource');
      }
    },

    async addLabAssignment() {
      if (!this.newLabAssignment.course_id || !this.newLabAssignment.title || !this.newLabAssignment.ex_input || !this.newLabAssignment.ex_output) {
        alert('Course, title, example input, and example output are required!');
        return;
      }

      try {
        console.log(this.newLabAssignment);
        const response = await axios.post('http://127.0.0.1:5000/api/codingqs', this.newLabAssignment, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.labMessages.push(`Lab Assignment "${this.newLabAssignment.title}" added successfully!`);
        // this.loadLabAssignments(); // Reload lab assignments after adding
        this.newLabAssignment = {
          course_id: '',
          title: '',
          description: '',
          ex_input: '',
          ex_output: '',
        }; // Clear the input fields
      } catch (error) {
        console.error('Error adding lab assignment:', error);
        alert('Error adding lab assignment');
      }
    },
  }
}
</script>

<style scoped>
/* Add your styles here */
.course-card {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.course-image {
  margin-right: 15px;
}

.course-image img {
  width: 150px;
  height: 150px;
  border-radius: 5px;
}

.course-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.course-content router-link {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  text-decoration: none;
  margin-bottom: 10px;
}

.course-content .btn {
  align-self: flex-end;
}
</style>
