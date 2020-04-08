import {Job} from "../types/job";

export const jobsList: Job[] = [1, 2, 3, 4, 5, 6, 7, 8, 9].map((value => ({
    id: value,
    name: `Job #${value}`,
    repo: `https://bitbucket.org/fxqlabs-oss/${value}`
})));