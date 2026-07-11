import {formatValue} from "../../utils/format";

type InfoRowProps = {
    label: string;
    value: unknown;
};

export function InfoRow({label, value}: InfoRowProps) {
    return (
        <div>
            <dt className="text-xs font-medium uppercase text-slate-500">{label}</dt>
            <dd className="mt-1 break-words text-slate-800">{formatValue(value)}</dd>
        </div>
    );
}
