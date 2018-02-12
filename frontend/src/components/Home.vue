<template>
  <div>
    <p>Home</p>
    <input
      type="text"
      placeholder="djibril.cisse@gmail.com"
      v-model="emailAddress"
    >
    <button @click="getEmailValidity">Verify Email</button>
    <br>
    <p>Email Validator Result: {{ validEmail }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      validEmail: '...',
      emailAddress: ''
    }
  },
  methods: {
    getEmailValidity () {
      this.validEmail = this.getEmailValidationFromBackend(this.emailAddress)
    },
    getEmailValidationFromBackend (emailAddress) {
      const path = `http://localhost:5000/api/email-validator` + '?email=' + emailAddress
      axios.get(path)
        .then(response => {
          this.validEmail = response.data.validEmail
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
