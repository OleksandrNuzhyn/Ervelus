import { defineStore } from 'pinia';
import api from '@/services/api';

export const useProductsStore = defineStore('products', {
    state: () => ({
        styles: [],
        genres: []
    }),
    actions: {
        async getStyles() {
            try {
                const { data } = await api.get('/api/products/styles/');
                this.styles = data || [];

                if (this.styles.length > 0) {
                    const genreMap = new Map();
                    this.styles.forEach(style => {
                        if (style.genre && style.genre.name && !genreMap.has(style.genre.name)) {
                            genreMap.set(style.genre.name, { id: style.genre.name, name: style.genre.name });
                        }
                    });
                    this.genres = Array.from(genreMap.values());
                }
                else {
                    this.genres = [];
                }
            }
            catch (error) {
                this.styles = [];
                this.genres = [];
            }
        }
    }
});