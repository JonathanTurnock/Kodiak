import {Run} from "../types/run";
import {addMinutes, subMinutes} from 'date-fns'

export const runsList: Run[] = [1, 2, 3, 4, 5, 6, 7, 8, 9].map((value => {
    const started = subMinutes(Date.now(), Math.random() * 100)
    const ended = addMinutes(started, Math.random() * 10)

    return {
        id: value,
        job_id: Math.round(Math.random() * 10),
        started: started,
        ended: ended,
        status: 1
    }
}));