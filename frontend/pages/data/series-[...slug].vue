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
              buttonTitle: 'Save',
              bannerText: bannerError,
            }"
            @submit.prevent="handleSave"
          >
            <ActivityFormInput
              @update:inputValue="dataPoint.data.label = $event"
              label="Data Label"
              v-bind="{
                placeholder: 'Label',
                required: true,
                inputValue: dataPoint.data.label,
              }"
            />
            <ActivityFormInput
              @update:inputValue="dataPoint.data.description = $event"
              label="Data Description"
              v-bind="{
                placeholder: 'Description',
                required: false,
                inputValue: dataPoint.data.description,
              }"
            />
            <ActivityFormAmountInput
              @update:amountValue="dataPoint.data.amount = $event"
              label="Data Amount"
              v-bind="{
                placeholder: '0',
                required: true,
                amountValue: dataPoint.data.amount,
              }"
            />
            <template #buttons>
              <button class="add-node-button" @click.stop.prevent="addEvent()">
                +
              </button>
              <button
                class="clear-nodes-button"
                @click.stop.prevent="clearAllNodes()"
              >
                Clear All
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

  type DataEventProps = {
    fieldSetId: number;
    data: DataEvent;
  };

  const bannerError = ref("");
  const dataPoint = ref<DataEventProps>({
    fieldSetId: 0,
    data: {
      label: "",
      description: "",
      date: new Date(),
      amount: 0,
    },
  });

  //retrieve series data
  onBeforeMount(() => {
    series = dataStore.getSeries(route.params.slug as string);
  });

  const handleSave = () => {
    console.log(dataPoint.value);
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
      "A A A A  A A B B  B B B B  B B B B"
      "A A A A  A A B B  B B B B  B B B B"
      "A A A A  A A B B  B B B B  B B B B"
      "A A A A  A A B B  B B B B  B B B B"
      "A A A A  A A B B  B B B B  B B B B"
      "C C C C  C C C C  C C C C  C C C C"
      "C C C C  C C C C  C C C C  C C C C"
      "C C C C  C C C C  C C C C  C C C C"
      "C C C C  C C C C  C C C C  C C C C"
      "C C C C  C C C C  C C C C  C C C C";
  }

  .edit-area {
    grid-area: A;
    width: 100%;
    max-height: 100%;
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
