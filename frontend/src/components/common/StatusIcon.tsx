import {AlertTriangle, Loader2, ShieldAlert, ShieldCheck} from "lucide-react";

import type {SafetyState} from "../../types/analyze";

type StatusIconProps = {
    state: SafetyState;
    isLoading: boolean;
};

export function StatusIcon({state, isLoading}: StatusIconProps) {
    const baseClasses = "flex h-12 w-12 items-center justify-center rounded-lg";

    if (isLoading) {
        return (
            <div className={`${baseClasses} bg-slate-100 text-slate-600`}>
                <Loader2 className="h-6 w-6 animate-spin" aria-hidden="true"/>
            </div>
        );
    }

    if (state === "danger") {
        return (
            <div className={`${baseClasses} bg-red-100 text-red-700`}>
                <ShieldAlert className="h-6 w-6" aria-hidden="true"/>
            </div>
        );
    }

    if (state === "safe") {
        return (
            <div className={`${baseClasses} bg-emerald-100 text-emerald-700`}>
                <ShieldCheck className="h-6 w-6" aria-hidden="true"/>
            </div>
        );
    }

    return (
        <div className={`${baseClasses} bg-amber-100 text-amber-700`}>
            <AlertTriangle className="h-6 w-6" aria-hidden="true"/>
        </div>
    );
}
