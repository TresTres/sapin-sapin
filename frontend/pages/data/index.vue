<template>
  <Activity>
    <template #header>User Financial Data</template>
    <template #content>
      <div class="content-container">
        <CommonCard class="context-display">
          <ActivityForm
            v-bind="{
              title: 'Create Data Series',
              buttonTitle: 'Create',
              bannerText: bannerError,
              descriptionValue:
                'All you need for a new data series is a unique title.',
            }"
            @submit="handleSeriesCreation"
          >
            <ActivityFormInput
              v-model:inputValue="seriesTitle"
              :label="seriesTitleLabel"
              :index="0"
              placeholder="Monthly Grocery Budget"
              required
            />
            <ActivityFormInput
              v-model:inputValue="description"
              :inputType="FormInputType.AREA"
              :label="seriesDescriptionLabel"
              :index="1"
              placeholder="Does not include department store purchases."
            />
          </ActivityForm>
        </CommonCard>
        <CommonCard class="series-display">
          <ul>
            <li v-for="[title, series] of dataStore.allSeries" :key="series.id">
              <NuxtLink :to="`/data/series-${title}`">
                <h3>{{ title }}</h3>
                <p>{{ series.description }}</p>
              </NuxtLink>
            </li>
          </ul>
        </CommonCard>
      </div>
    </template>
  </Activity>
</template>

<script lang="ts" setup>
  definePageMeta({
    title: "User Financial Data",
    layout: "dashboard",
  });
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
        dataStore.replaceSeries(
          proposedSeries.title,
          response as DataEventSeries
        );
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
</script>

<style lang="scss" scoped>
  .content-container {
    display: grid;
    width: 100%;
    height: 100%;
    align-items: stretch;

    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat(7, 1fr);

    gap: 4rem;

    padding: $medium-large-text-size;

    grid-template-areas:
      "A A A A   A B B B  B B B B"
      "A A A A   A B B B  B B B B"
      "A A A A   A B B B  B B B B"
      "A A A A   A B B B  B B B B"
      "C C C C   C B B B  B B B B"
      "C C C C   C B B B  B B B B"
      "C C C C   C B B B  B B B B";
  }

  .context-display {
    grid-area: A;
  }

  .series-display {
    display: flex;
    flex-direction: column;

    grid-area: B;

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
