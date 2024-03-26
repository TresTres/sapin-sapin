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
              {{ series.title + " - " + series.id }}
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
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: $medium-large-text-size;
  }
  
  .series-display {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: $medium-large-text-size;

    width: 50%;

    border: 1px solid $dark-orange-color;
  }
</style>