<script setup lang="ts">
// example usage of api instance
// In a composable or component
import api from '../services/api'

const createItem = async (itemData: { name: string }) => {
  try {
    const response = await api.post('/items', itemData)
    return response.data
  } catch (error) {
    // handle error
  }
}
</script>