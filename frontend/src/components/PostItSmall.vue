<template>
  <div v-draggable.move="postit.id">
  <li
    class="post-it-small"
    :class="postit.status"
    @click="$emit('post-it-selected');"
    @mouseover="$emit('posit-mouseover')"
    v-tooltip.top-center="text_ttip"
  >
  {{text}}
  </li>
  </div>
</template>

<script>
export default {
  name: "PostItSmall",
  props: ["postit"],
  computed: {
    text(){
      // Text to show inside the postit.
      if (this.postit.title.length < 40)
        return this.postit.title;
      return this.postit.title.slice(0, 39) + '...';
    },
    text_ttip(){
      return this.postit.title > this.text ? this.postit.title : ""
    }
  },
};
</script>

<style>
.post-it-small {
  position: relative;
  list-style: none;
  color: white;
  text-align: center;
  max-width: 10rem;
  max-height: 6rem;
  margin-right: 1rem;
  margin-bottom: 1.2rem;
  padding: 0.7rem 1rem;
  border-radius: 2px;
  box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition-property: transform, filter;
  transition-duration:  0.15s;
  filter: brightness(1);
  transform: rotate(2deg);
  z-index: 0;
  font-weight: 500;
  overflow-wrap: break-word;
  overflow-y: hidden;
}

.post-it-small:nth-child(2n){
  transform: rotate(-2deg);
}

.post-it-small:nth-child(3n){
  transform: rotate(2deg);
}

.post-it-small:nth-child(4n-1){
  transform: rotate(-3deg);
}

.post-it-small:nth-child(8n-1){
  transform: rotate(3deg);
}

.post-it-small:hover{
  transform: scale(1.25);
  filter: brightness(1.1);
  z-index: 100;
}


/* Colors for the different states of the post-its */

.O{ /* Open */
  background-color: #FDD835;
  color: var(--dark);
}

.A{ /* Approved */
  background-color: var(--green);
  color: white;
}

.R{ /* Rejected */
  background-color:var(--red);
  color: white;
}

/* Tooltip */
.tooltip {
  display: block !important;
  z-index: 10000;
}
 
.tooltip .tooltip-inner {
  background: black;
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}
 
.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: black;
  z-index: 1;
}
 
.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}
 
.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}
 
.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}
 
.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}
 
.tooltip[x-placement^="right"] {
  margin-left: 5px;
}
 
.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}
 
.tooltip[x-placement^="left"] {
  margin-right: 5px;
}
 
.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}
 
.tooltip.popover .popover-inner {
  background: #f9f9f9;
  color: black;
  padding: 24px;
  border-radius: 5px;
  box-shadow: 0 5px 30px rgba(black, .1);
}
 
.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}
 
.tooltip[aria-hidden='true'] {
  visibility: hidden;
  opacity: 0;
  transition: opacity .15s, visibility .15s;
}
 
.tooltip[aria-hidden='false'] {
  visibility: visible;
  opacity: 1;
  transition: opacity .15s;
}
</style>