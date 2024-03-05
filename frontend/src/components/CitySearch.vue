<template>
  <div class="form-control">
    <label for="city-search" class="cool-label">Find Your City</label>
    <input id="city-search" name="city-search" type="text" v-model="searchTerm" placeholder="Search for a city" class="cool-input"/>
  </div>

  <ul v-if="!selectedCity" class="user-list cool-user-list">
    <li v-for="city in filteredCities" :key="city.id" @click="selectCity(city)" :class="{ 'selected-city': selectedCity === city }">
      <div class="user-info">
        <img :src="require('/public/city_icon.svg')" alt="City Icon" class="city-icon">
        <div class="city-info">
          <h4>{{ city.name }}</h4>
          <p>{{ city.country_code }}</p>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      cities: [],
      searchTerm: '',
      selectedCity: null
    }
  },
  created() {
    this.getData();
  },
  computed: {
    filteredCities() {
      return this.cities.filter(city => {
        return (
            city.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
            city.country_code.toLowerCase().includes(this.searchTerm.toLowerCase())
        );
      });
    }
  },
  methods: {
    async getData() {
      try {
        const res = await fetch('http://127.0.0.1:8000/cities');
        const data = await res.json();
        this.cities = data.cities;
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    selectCity(city) {
      this.selectedCity = city;
      this.searchTerm = `${city.name}, ${city.country_code}`;
      this.$emit('update:modelValue', this.searchTerm)
    }
  }
}
</script>

<style scoped>
.cool-label {
  font-weight: bold;
  color: #444;
}

.cool-input {
  display: block;
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

.cool-input:focus {
  outline: none;
  border-color: #0076bb;
}

.city-icon {
  width: 50px; /* Set width and height to desired size */
  height: 50px;
  object-fit: cover; /* Maintain aspect ratio */
  border-radius: 50%; /* Make the image circular */
  margin-right: 10px; /* Add space between icon and text */
}

.cool-user-list {
  background-color: white;
  list-style-type: none;
  margin: 0;
  max-height: 250px;
  overflow-y: auto;
}

.cool-user-list li {
  padding: 10px;
  padding-left: 0;
  margin-left: 0;
  cursor: pointer; /* Add cursor pointer */
  transition: background-color 0.3s ease; /* Smooth transition */
}

.cool-user-list li.selected-city {
  background-color: #ddd; /* Change background color for selected city */
}

.user-info {
  display: flex;
  align-items: center;
}

.city-info {
  display: flex;
  flex-direction: column;
}

.city-info h4 {
  margin: 0 0 5px 0;
  font-size: 16px; /* Adjust the font size as needed */
}

.city-info p {
  margin: 0;
  font-size: 14px; /* Adjust the font size as needed */
}

.cool-user-list li:hover {
  background-color: #f0f0f0; /* Change background color on hover */
}
</style>
