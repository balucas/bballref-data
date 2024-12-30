import axios from 'axios';
import { fetchGamelogs } from './api';
import { mockGamelogData } from './mockData';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('fetchGamelogs', () => {
    it('should fetch gamelogs successfully', async () => {
        const playerId = 'jokicni01';
        const stats = ['pts', 'ast', 'blk'];
        const num = 10;

        mockedAxios.get.mockResolvedValueOnce({ data: mockGamelogData });

        const result = await fetchGamelogs(playerId, stats, num);

        expect(result).toEqual(mockGamelogData);
        expect(mockedAxios.get).toHaveBeenCalledWith(
            `http://127.0.0.1:5000/gamelog/${playerId}`,
            { params: new URLSearchParams({ stats: stats.join(','), num: num.toString() }) }
        );
    });

    it('should throw an error if the request fails', async () => {
        const playerId = '12345';
        const stats = ['points', 'rebounds'];
        const num = 10;
        const mockError = new Error('Network Error');

        mockedAxios.get.mockRejectedValueOnce(mockError);

        await expect(fetchGamelogs(playerId, stats, num)).rejects.toThrow('Network Error');
    });
});