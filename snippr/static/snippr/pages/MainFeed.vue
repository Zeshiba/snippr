<template>
	<div class="columns is-centered feed">
		<div class="column is-8">
			<div class="columns is-marginless">
				<div class="column is-paddingless is-narrow">
					<div class="tabs is-toggle has-background-white">
						<ul>
							<li :class="{'is-active': statusFilter == 'O'}">
								<router-link :to="{name: 'feed', query: submitFilter(filterset, {status: 'Open'})}">
									<span class="tab-item">Open</span>
									<span class="tag is-light">{{
										openCount
									}}</span>
								</router-link>
							</li>
							<li :class="{'is-active': statusFilter == 'C'}">
								<router-link :to="{name: 'feed', query: submitFilter(filterset, {status: 'Closed'})}">
									<span class="tab-item">Closed</span>
									<span class="tag is-light">{{
										closedCount
									}}</span>
								</router-link>
							</li>
							<li :class="{'is-active': !statusFilter}">
								<router-link :to="{name: 'feed', query: submitFilter(filterset, {status: 'All'})}">
									<span class="tab-item">All</span>
									<span class="tag is-light">{{
										allCount
									}}</span>
								</router-link>
							</li>
						</ul>
					</div>
				</div>
				<div class="column is-paddingless">
					<router-link :to="{ name: 'createissue' }" class="button is-success is-pulled-right">New Issue</router-link>
				</div>
			</div>
			<div class="columns search-bar">
				<div class="column box">
					<FormInput
						type="text"
						class="has-addons"
						placeholder=""
						:value="search"
						inputClass="input"
						v-model="search"
						>
						<div slot="addon" class="control">
							<LanguageFilter 
								:value="languageFilter"
								@filter="filter"
								:hasFilterAll="hasFilterAll"
							/>
						</div>
						<div slot="right-addon" class="control">
							<router-link :to="{name: 'feed', query: submitFilter(filterset, {filter: languageFilter, title: searchText()})}" class="button is-link">Search</router-link>
						</div>
					</FormInput>
				</div>
			</div>
			<div class="box snippet-list">
				<SnippetRow v-for="snippet in snippets" :snippet="snippet" :key="snippet.pk" />
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'source/plugins/axios';
import moment from 'moment';

import FormInput from "../components/_generics/FormInput.vue";
import SnippetRow from "../components/feed/SnippetRow.vue";
import LanguageFilter from "../components/filters/LanguageFilter.vue";
export default {
  name: "MainFeed",

  components: {
    FormInput,
    LanguageFilter,
    SnippetRow
  },

  data() {
    return {
      tabOption: 0,
      search: "",
      filterset: {},
      snippets: null,
      register: false,
      statusFilter: false,
      languageFilter: 'All',
      hasFilterAll: true,
      openCount: 0,
      closedCount: 0,
      allCount: 0,
    };
  },

  methods: {
    filter(value){
    	this.languageFilter = value
    },
    submitFilter(old, add){
    	return Object.assign({}, old, add);
    },
    searchText(){
    	if(this.search == ""){
    		return "All";
    	} else {
    		return this.search
    	}
    }
  },

  async mounted() {

  	this.filterset = this.$route.query
    let headers = {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    };
    let languageFilter = null
    let query = 'https://1b7c4ba8.ngrok.io/api/commit' 
    let route = this.$route.query
    if(route.filter || route.status || route.title){
    	query = query + '?'
	    if(route.filter && route.filter != 'All'){
	    	languageFilter = route.filter
	    	this.languageFilter = route.filter
	    	query = query + 'language=' + languageFilter + '&'
	    }
	    if(route.title && route.title != "All"){
	    	this.search = route.title
	    	query = query + 'title=' + this.search + '&'
	    }
	    if(route.status){
	    	let status = route.status
	    	if (status == 'Open') {
	    		query = query + 'status=O'
	    		this.statusFilter = 'O'
	    	} else if (status == 'Closed'){
	    		query = query + 'status=C'
	    		this.statusFilter = 'C'
	    	} else {
	    		this.statusFilter = null
	    	}
	    }
    }
    if(!this.$route.query.filter && !this.$route.query.status){
    	query = query + '/'
    }
    
    
    let response = await axios.get(query, headers);
    console.log(response.results)
    this.snippets = response.results.commits;
    this.openCount = response.results.open_count
    this.closedCount = response.results.closed_count
    this.allCount = response.results.all_count
  }
};
</script>

<style scoped>
.tabs {
  margin-bottom: 0px;

  .tab-item {
    margin-right: 8px;
  }
}

.search-bar {
  margin: 12px 0px;
}

.snippet-list {
	padding-left: 40px;
	padding-right: 40px;
}

</style>