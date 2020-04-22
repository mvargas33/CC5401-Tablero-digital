<template>
  <b-modal
    id="board-details-modal"
    title="Detalles del tablero"
    hide-footer
    body-class="board-details-body"
    header-text-variant="info"
    content-class="border-info"
    header-close-variant="info"
  > 
    <table
      id="board-detail-table"
    >
      <tr>
        <th scope="row">Nombre</th>  
        <td>{{ board.name }}</td>  
      </tr>
      <tr>
        <th scope="row">Descripción</th>  
        <td>{{ board.description }}</td>
      </tr>
      <tr>
        <th scope="row">Propietario</th>
        <td>{{ owner.full_name == undefined? '-': owner.full_name}}</td>
      </tr>
    </table>
    
  </b-modal>
</template>

<script>
export default {
  name: 'BoardDetailsModal',
  props: {
    board: Object,
    owner: Object,
  }
}
</script>

<style>
#board-detail-table td:nth-child(2){
  padding-left: 1rem;
}

#board-detail-table tr:not(:first-child) td,
#board-detail-table tr:not(:first-child) th{
  padding-top: 0.5rem;
}

#board-detail-table td,
#board-detail-table th{
  vertical-align: top;
}

#board-detail-table th{
  color: var(--secondary);
}

.board-details-body{
  min-height: 9rem;
  display: flex;
  align-items: center;
}
</style>