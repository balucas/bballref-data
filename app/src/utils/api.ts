import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const fetchGamelogs = async (playerId: string, stats: Array<string>, num: number) => {
    try {
        // Form query parameters
        const params = new URLSearchParams();
        params.append('stats', stats.join(','));
        params.append('num', num.toString());

        const response = await axios.get(`${API_BASE_URL}/gamelog/${playerId}`, { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};
