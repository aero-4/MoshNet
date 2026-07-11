import {ShieldCheck} from "lucide-react";

export function AppHeader() {
    return (
        <header className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-slate-900 text-white">
                    <ShieldCheck className="h-6 w-6" aria-hidden="true"/>
                </div>
                <div>
                    <h1 className="text-2xl font-semibold tracking-normal text-slate-950">
                        netMosh
                    </h1>
                </div>
            </div>
        </header>
    );
}
