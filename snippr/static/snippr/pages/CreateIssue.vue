<template>
    <div class="columns is-centered">
    	<div class="column is-8 box">
    		<div class="columns is-marginless">
    			<div class="column level">
						<div class="level-item vertical content">
							<p class="title has-text-primary">
								New Issue
							</p>
							<p class="subtitle"><small>Have you experience a problem on your code? Ask for help in our community.</small></p>
						</div>
					</div>
    		</div>
    		<hr class="is-marginless">
    		<div class="columns is-centered is-marginless">
    		  <div class="column is-10">
						<HorizontalFormInput
						  class="issue-input"
					    type="text"
					    label="Title"
					    placeholder="My First Issue"
					    v-bind:value="title"
					    inputClass="input"
					    v-model="title"
					  />
						<HorizontalFormInput
						  class="issue-input"
							type="textarea"
							label="Description"
							placeholder="My First Issue"
							v-bind:value="description"
							inputClass="textarea has-fixed-size"
							v-model="description"
							rows="5"
						/>
						<div class="field is-horizontal">
							<div class="field-label is-normal">
								<label class="label">Language</label>
							</div>
							<div class="field-body">
								<div class="field is-narrow">
									<div class="control">
										<LanguageFilter
										 :value="language"
										 @filter="selectLanguage"
										/>
									</div>
								</div>
							</div>
						</div>
						<hr>
						<HorizontalFormInput
							type="textarea"
							label="Code"
							placeholder="My First Issue"
							v-bind:value="code"
							inputClass="textarea has-fixed-size snippet"
							v-model="code"
							rows="5"
						/>
    		  </div>
    		</div>
    		<hr>
    		<div class="columns is-centered is-marginless">
    			<div class="column is-12 is-flex justify-between">
    				<button class="button is-success" @click="submit">Submit Issue</button>
    				<button class="button is-outlined" @click="cancel">Cancel</button>
    			</div>
    		</div>
    	</div>
    </div>
</template>

<script>
import axios from 'axios';

import LanguageFilter from "../components/filters/LanguageFilter.vue";
import HorizontalFormInput from "../components/_generics/HorizontalFormInput.vue";
export default {
  name: "CreateIssue",

  components: {
    HorizontalFormInput,
    LanguageFilter
  },

  data() {
    return {
      title: "",
      description: "",
      language: "C",
      code: ""
    };
  },

  methods: {
    async submit() {
      let payload = {
        title: this.title,
        description: this.description,
        language: this.language,
        code: this.code
      };

      let headers = {
        headers: {
          'AUTHORIZATION': `Bearer ${localStorage.getItem('token')}`
        }
      };

      let response = await axios.post('https://1b7c4ba8.ngrok.io/api/commit/', payload, headers);

      if(response.data.message === "successfully created") {
        this.$router.push({ 
          name: 'issue', 
          params: { 
            id: response.data.pk
          } 
        });
      }
    },

    selectLanguage(value){
    	this.language = value
    },

    cancel() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.feed {
  padding-top: 2rem;
}
.tabs {
  margin-bottom: 0px;

  .tab-item {
    margin-right: 8px;
  }
}

.search-bar {
  margin: 12px;
}

.vertical {
  flex-direction: column;
}

.flex-right {
  align-items: flex-end !important;
}

.flex-vertical-center {
  display: flex;
  align-items: center;
}

.has-bottom-border {
  border-bottom: 1px solid hsl(0, 0%, 86%);
}

.file-input {
  opacity: 0;
}
</style>