import {ShieldCheck} from "lucide-react";

export function AppHeader() {
    return (
        <header className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
            <a className="flex items-center gap-3" href="/">
                <ShieldCheck className="h-6 w-6" aria-hidden="true"/>
                <div>
                    <h1 className="text-2xl font-semibold tracking-normal text-slate-950">
                        NetMoshen
                    </h1>
                </div>
            </a>
        </header>
    );
}
