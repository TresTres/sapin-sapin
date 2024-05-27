<template>
  <ActivityShell>
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
            @submit.prevent="handleSeriesCreation"
          >
            <ActivityFormInput
              v-model:inputValue="seriesTitle"
              :label="seriesTitleLabel"
              placeholder="Monthly Grocery Budget"
              required
            />
            <ActivityFormInput
              v-model:inputValue="description"
              :input-type="FormInputType.AREA"
              :label="seriesDescriptionLabel"
              placeholder="Does not include department store purchases."
            />
          </ActivityForm>
        </CommonCard>
        <CommonCard class="series-display">
          <ul>
            <li
              v-for="[title, series] of dataStore.allSeriesEntries"
              :key="series.id"
            >
              <NuxtLink :to="`/data/series-${title}`" class="series-link">
                <div class="series-box">
                  <h3>{{ title }}</h3>
                  <p>{{ series.description }}</p>
                </div>
              </NuxtLink>
            </li>
          </ul>
        </CommonCard>
      </div>
    </template>
  </ActivityShell>
</template>

<script lang="ts" setup>
definePageMeta({
  title: "User Financial Data",
  layout: "dashboard",
});
// series creation form
const seriesTitleLabel = "New Series Title";
const seriesDescriptionLabel = "New Series Description";
const seriesTitle = ref<string>("");
const description = ref<string>("");
const bannerError = ref("");

const dataStore = useDataStore();

// get series
onBeforeMount(async () => {
  const { ownedSeries } = await useAuthorizingFetch("/api/data/series");
  dataStore.loadMultipleSeries(ownedSeries as DataEventSeries[]);
});

const handleSeriesCreation = async (): Promise<void> => {
  /*
   * Attempt to create a new data series, and display an error if the series cannot be created.
   */
  if (dataStore.has(seriesTitle.value)) {
    bannerError.value = "Series already exists";
    return;
  }
  // update UI
  const proposedSeries: DataEventSeries = {
    id: "-0",
    title: seriesTitle.value,
    description: description.value,
    events: [],
    recurrences: [],
  };
  dataStore.addSeries(proposedSeries);
  // POST to server
  await useAuthorizingFetch("/api/data/series", {
    method: "POST",
    body: JSON.stringify(proposedSeries),
  })
    .then((response) => {
      // replace element on success and cleanup
      dataStore.replaceSeries(
        proposedSeries.title,
        response as DataEventSeries,
      );
      seriesTitle.value = "";
    })
    .catch((error) => {
      // display error in form banner
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

  gap: 2rem;

  padding: $standard-text-size;

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

  overflow: auto;

  li {
    list-style: none;

    margin: 0.3rem;
    padding: 0.3rem;
    border-radius: 0.5rem;
    border: 3px solid transparent;

    transition:
      background-color 0.5s ease-in-out,
      border 0.5s ease-in-out;

    &:hover {
      background-color: adjust-alpha($dark-purple-color, 60%);
      border: 3px solid $primary-orange-color;
    }

    background-color: adjust-alpha($dark-purple-color, 45%);

    .series-link {
      color: $primary-orange-color;
      text-decoration: none;
      color: $primary-orange-color;

      .series-box {
        padding: 1rem 1rem;
      }

      h3 {
        text-transform: capitalize;
      }
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
