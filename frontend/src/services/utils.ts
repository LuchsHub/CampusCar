import type { CodriveCardProps, LocationItemProps } from "@/types/Props";
import type { RideGetDto } from "@/types/Ride";

export const formatDate = (date: string) => {
    const [year, month, day] = date.split('-');
    return `${day}.${month}.${year.slice(2)}`;
}

export const formatTime = (time: string) => {
    const [hour, minute] = time.split(':');
    return `${hour}:${minute}`;
}

export const sortRidesByDateAsc = (rides: RideGetDto[]): RideGetDto[] => {
    return [...rides].sort((a, b) => {
        const aDate = new Date(`${a.departure_date}T${a.departure_time}`);
        const bDate = new Date(`${b.departure_date}T${b.departure_time}`);
        return aDate.getTime() - bDate.getTime();
    });
}

export const sortLocationItemPropsByTimeAsc = (items: LocationItemProps[]): LocationItemProps[] => {
    const today = new Date().toISOString().slice(0, 10); 
    return [...items].sort((a, b) => {
        const aDate = new Date(`${today}T${a.arrival_time}`);
        const bDate = new Date(`${today}T${b.arrival_time}`);
        return aDate.getTime() - bDate.getTime();
      });
}

export const sortCodriveCardPropsByTimeAsc = (items: CodriveCardProps[]): CodriveCardProps[] => { 
    return [...items].sort((a, b) => {
        const aDate = new Date(`${a.codrive.arrival_date}T${a.codrive.arrival_time}`);
        const bDate = new Date(`${b.codrive.arrival_date}T${b.codrive.arrival_time}`);
        return aDate.getTime() - bDate.getTime();
      });
}