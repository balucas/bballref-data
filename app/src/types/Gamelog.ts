export interface Gamelog {
    _id: { 
        player_id: string; 
        game_id: string 
    };
    date_game: string;
    season: string;
    status: string;
    opp_id: string;
    [key: string]: string | number | { player_id: string; game_id: string; };
}

export function getField<T>(obj: T, field: string): T[keyof T]{
    return obj[field as keyof T];
}