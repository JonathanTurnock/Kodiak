import React from "react";

export interface NavbarLink {
    path: string,
    name: string,
    component: React.FC
}