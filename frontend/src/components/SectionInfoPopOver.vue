<template>
  <b-popover
    :target="target"
    triggers="hover"
    placement="bottom"
    variant="info"
    custom-class="section-info"
  >
    <template v-slot:title>
      <span class="text-info">
        <font-awesome-icon
          class="mr-1"
          icon="info-circle"
        />
        {{ section.title }}
      </span>
    </template>
    {{ section.description }}
  </b-popover>
</template>

<script>
export default {
  name: 'SectionInfoPopOver',
  props: {
    section: Object,
    target: String,
  }
}
</script>

<style>

.section-info{
  margin-left: 1rem;
}

</style>