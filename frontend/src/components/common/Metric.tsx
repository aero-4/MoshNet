type MetricProps = {
    label: string;
    value: number;
};

export function Metric({label, value}: MetricProps) {
    return (
        <div className="rounded-md bg-slate-50 px-3 py-3">
            <div className="text-xs font-medium uppercase text-slate-500">{label}</div>
            <div className="mt-1 text-2xl font-semibold text-slate-950">{value}</div>
        </div>
    );
}
