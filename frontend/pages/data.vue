<template>
  <Activity>
    <template #header>User Financial Data</template>
    <template #bar>
      <button
        type="button"
        class="activity-form-toggle-button"
        @click.prevent="toggleActivityForm"
      >
        {{ showActivityFormText }}
      </button>
      
    </template>
    <template #content>
      <div class="content-container">
        <div class="context-display">
          <div class="activity-form">
            <ActivityForm
              v-show="showActivityForm"
              v-bind="{
                title: 'Create Data Series',
                buttonTitle: 'Create',
                bannerText: bannerError,
                descriptionValue: 'All you need for a new data series is a unique title.'
              }"
              @submit="handleSeriesCreation"
            >
              <ActivityFormInput
                v-model:inputValue="seriesTitle"
                :label="seriesTitleLabel"
                :index="0"
                placeholder="Monthly Grocery Budget"
              />
            </ActivityForm>
          </div>
        </div>
        <div class="series-display">
          <ul>
            <li v-for="[title, series] of dataStore.allSeries" :key="series.id">
              <h3> {{ title }} </h3>
              <p> {{  series.description }}</p>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </Activity>
</template>

<script lang="ts" setup>
  definePageMeta({
    title: "User Financial Data",
    layout: "dashboard",
  });
  //activity
  const showActivityForm = ref(false);
  const showActivityFormText = ref("Create Data Series");
  //series creation form
  const seriesTitleLabel = "New Series Title";
  const seriesDescriptionLabel = "New Series Description";
  const seriesTitle = ref("");
  const description = ref("");
  const bannerError = ref("");

  const dataStore = useDataStore();

  //get series
  onBeforeMount(async () => {
    const { owned_series } = await useAuthorizingFetch("/api/data/series");
    dataStore.loadMultipleSeries(owned_series as DataEventSeries[]);
  });

  const handleSeriesCreation = async (): Promise<void> => {
    /*
     * Attempt to create a new data series, and display an error if the series cannot be created.
     */
    if (dataStore.doesSeriesExist(seriesTitle.value)) {
      bannerError.value = "Series already exists";
      return;
    }
    // update UI
    const proposedSeries: DataEventSeries = {
      id: "-0",
      title: seriesTitle.value,
      description: description.value,
    };
    dataStore.addSeries(proposedSeries);
    // POST to server
    await useAuthorizingFetch("/api/data/series", {
      method: "POST",
      body: JSON.stringify(proposedSeries),
    })
    .then((response) => {
      // replace element on success and cleanup
      // console.log(response);
      dataStore.replaceSeries(proposedSeries.title, response as DataEventSeries);
      showActivityForm.value = false;
      showActivityFormText.value = "Create Data Series";
      seriesTitle.value = "";
    })
    .catch((error) => {
      // display error in form banner
      // console.log(error);
      if (error.data) {
        const { message } = error.data;
        bannerError.value = message;
        return;
      }
      bannerError.value = error;
    });
  };

  const toggleActivityForm = () => {
    showActivityForm.value = !showActivityForm.value;
    showActivityFormText.value = !!showActivityForm.value
      ? "Hide Form"
      : "Create Data Series";
  };
</script>


<style lang="scss" scoped>
  .content-container {
    display: grid;
    width: 100%;
    height: 100%;
    align-items: stretch;

    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat(8, 1fr);

    gap: 4rem;

    padding: $medium-large-text-size;

    grid-template-areas:
      "A A A A   B B B B  C C C C"
      "A A A A   B B B B  C C C C"
      "A A A A   B B B B  D D D D"
      "A A A A   B B B B  D D D D"
      "A A A A   B B B B  D D D D"
      "A A A A   B B B B  D D D D"
      "A A A A   B B B B  D D D D"
      "A A A A   B B B B  D D D D";
  }

  .context-display {


    grid-area: A;
    padding: $medium-large-text-size;

    background-color: adjust-alpha($light-purple-color, 15%);
    @include small-box-shadow();

    border-radius: 1.3rem;
  }
  
  .series-display {


    display: flex;
    flex-direction: column;

    grid-area: B;
    padding: $medium-large-text-size;

    background-color: adjust-alpha($light-purple-color, 15%);
    @include small-box-shadow();

    border-radius: 1.3rem;

    li {
      list-style: none;

      margin: 0.5rem;

      padding: $small-text-size;
      border-radius: 0.5rem;

      
      color: $light-orange-color;
      background-color: adjust-alpha($dark-orange-color, 45%);

      h3 {
        text-transform: capitalize;
      }
    }
  }




  .activity-form-toggle-button {
    padding: 0.5rem 1.3rem;
  
    font-size: $medium-large-text-size;

    background-color: adjust-alpha($light-purple-color, 80%);
    color: $white-color;
    opacity: 0.8;
  
    border: none;
    border-radius: 0.75rem;
  
    &:hover {
      background-color: $white-color;
      color: $dark-purple-color;
    }
  }
</style>