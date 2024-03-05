<template>
  <form @submit.prevent="submitForm" class="cool-form">
    <div class="form-control" :class="{invalid: userNameValidity === 'invalid'}">
      <label for="user-name" class="cool-label">Your Name</label>
      <input id="user-name" name="user-name" type="text" v-model.trim="userName" @blur="validateInput('userName')"
             class="cool-input"/>
      <p v-if="userNameValidity === 'invalid'" class="error-message">Please enter a valid name</p>
    </div>

    <div class="form-control" :class="{invalid: emailValidity === 'invalid'}">
      <label for="email" class="cool-label">Your Email</label>
      <input id="email" name="email" type="email" v-model.trim="email" @blur="validateInput('email')" class="cool-input"/>
      <p v-if="emailValidity === 'invalid'" class="error-message">Please enter a valid email</p>
    </div>

    <div class="form-control">
      <CitySearch v-model="location"></CitySearch>
    </div>
    <div>
      <router-link v-if="isFormValid" :to="{ path: '/main', query: { account: email } }" @click="submitForm" class="cool-button">Save
        Data
      </router-link>
      <span v-else class="cool-button disabled">Save Data</span>

    </div>
  </form>
</template>

<script>
import CitySearch from "@/components/CitySearch";

export default {
  components: { CitySearch },
  data() {
    return {
      userName: '',
      email: '',
      location: '',
      userNameValidity: 'pending',
      emailValidity: 'pending'
    }
  },
  computed: {
    isFormValid() {
      return this.userNameValidity === 'valid' && this.emailValidity === 'valid' && this.userName.trim() !== '' && this.email.trim() !== '' && this.location.trim() !== '';
    }
  },
  methods: {
    validateInput(field) {
      if (field === 'userName') {
        this.userNameValidity = this.userName === '' ? 'invalid' : 'valid';
      } else if (field === 'email') {
        this.emailValidity = this.validateEmail(this.email) ? 'valid' : 'invalid';
      }
    },
    validateEmail(email) {
      const re = /\S+@\S+\.\S+/;
      return re.test(email);
    },
    submitForm() {
      if (this.userName.trim() === '' || this.email.trim() === '' || this.location.trim() === '') {
        this.userNameValidity = 'invalid';
        this.emailValidity = 'invalid';
        console.error('Please fill in all fields');
        return; // Stop the form submission
      }

      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.userName,
          email: this.email,
          location: this.location
        })
      };
      fetch('http://127.0.0.1:8000/register', options)
          .then(response => {
            if (response.ok) {
              console.log(this.options);
            }
          })
          .catch(error => {
            console.error('Error deleting row:', error);
          });
      this.userName = '';
      this.location = '';
      this.email = '';
    }
  }
}
</script>

<style scoped>
.cool-form {
  margin: 2rem auto;
  max-width: 40rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 2rem;
  background-color: #f0f0f0;
}

.form-control {
  margin-bottom: 1.5rem;
}

.invalid input {
  border-color: red;
}

.invalid .cool-label {
  color: red;
}

.cool-label {
  font-weight: bold;
  color: #444;
}

.error-message {
  color: red;
  margin-top: 0.5rem;
}

.cool-input,
.cool-select {
  display: block;
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

.cool-input:focus,
.cool-select:focus {
  outline: none;
  border-color: #0076bb;
}

.cool-button {
  text-decoration: none;
  font: inherit;
  border: none;
  background-color: #0076bb;
  color: white;
  cursor: pointer;
  margin-top: .75rem;
  padding: 0.75rem 2rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.cool-button:hover,
.cool-button:active {
  background-color: #005488;
}
</style>
