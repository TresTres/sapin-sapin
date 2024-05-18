import { Activity } from '../../.nuxt/components';
<template>
  <Activity>
    <template #header>
      <h2>{{ series?.title || "" }}</h2>
      <p>{{ series?.description || "" }}</p>
    </template>
    <template #content>
      <div class="content-container">
        <CommonCard class="edit-area">
          <ActivityForm
            v-bind="{
              title: 'Add Financial Transaction',
              buttonTitle: 'Add Point',
              bannerText: bannerError,
            }"
            @submit.prevent="handleSave"
          >
            <ActivityFormInput
              v-model:inputValue="dataPoint.label"
              v-bind="{
                label: 'Data Label',
                placeholder: 'Grocery Trip',
                required: true,
              }"
            />
            <ActivityFormInput
              v-model:inputValue="dataPoint.description"
              label="Data Description"
              v-bind="{
                placeholder: 'Description',
                required: false,
              }"
            />
            <fieldset class="small-fields"> 
              <div style="flex: 5">
                <ActivityFormAmountInput
                  v-model:amountValue="dataPoint.amount"
                  label="Data Amount"
                  v-bind="{
                    placeholder: '0',
                    required: true,
                  }"
                />
              </div>
              <div style="flex: 7">
                <ActivityFormDatetimeInput
                  v-model:dateValue="dataPoint.date"
                  label="Date"
                  v-bind="{
                    placeholder: '2010-10-10',
                    required: true,
                  }"
                />
              </div>
            </fieldset>

            <template #buttons>
              <button
                class="clear-nodes-button"
                @click.stop.prevent="resetDataPoint()"
              >
                Clear Fields
              </button>
            </template>
          </ActivityForm>
        </CommonCard>
        <div className="graph-area"></div>
        <div className="cells-area"></div>
      </div>
    </template>
  </Activity>
</template>

<script lang="ts" setup>
  definePageMeta({
    title: `User Series`,
    layout: "dashboard",
  });

  const route = useRoute();
  const dataStore = useDataStore();
  let series: DataEventSeries | null = null;

  //data event addition form
  const bannerError = ref("");
  const dataPoint = ref<DataEvent>({
    label: "",
    description: "",
    date: new Date(),
    amount: 0.00,
  });
  //retrieve series data
  onBeforeMount(() => {
    series = dataStore.getSeries(route.params.slug as string);
  });

  const handleSave = () => {
    console.log(dataPoint.value);
  };

  const resetDataPoint = () => {
    dataPoint.value = {
      label: "",
      description: "",
      date: new Date(),
      amount: 0.00,
    };
  };  
</script>

<style lang="scss" scoped>
  .content-container {
    display: grid;
    width: 100%;
    height: 100%;
    align-items: stretch;

    grid-template-columns: repeat(16, 1fr);
    grid-template-rows: repeat(8, 1fr);

    gap: 2rem;

    padding: $standard-text-size;

    grid-template-areas:
      "A A A A  A A A B  B B B B  B B B B"
      "A A A A  A A A B  B B B B  B B B B"
      "A A A A  A A A B  B B B B  B B B B"
      "A A A A  A A A B  B B B B  B B B B"
      "A A A A  A A A B  B B B B  B B B B"
      "C C C C  C C C B  B B B B  B B B B"
      "C C C C  C C C B  B B B B  B B B B"
      "C C C C  C C C B  B B B B  B B B B"
      "C C C C  C C C B  B B B B  B B B B"
      "C C C C  C C C B  B B B B  B B B B";
  }

  .edit-area {
    grid-area: A;
    width: 100%;
    max-height: 100%;
  }

  .small-fields {
    
    border: none;
    display: flex;
    flex-direction: row;

    gap: $small-text-size
  }

  .add-node-button {
    @include large-button;

    width: 30%;

    font-weight: $bold-text-weight;

    background-color: $primary-orange-color;
    color: $white-color;

    &:hover {
      background-color: $light-orange-color;
      color: $dark-red-color;
    }
  }

  .clear-nodes-button {
    @include large-button;

    width: 20%;
    left: 0;

    background-color: $dark-red-color;
    color: $white-color;

    &:hover {
      background-color: $light-red-color;
      color: $dark-red-color;
    }
  }
</style>
