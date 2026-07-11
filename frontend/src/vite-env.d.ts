interface ImportMetaEnv {
    readonly VITE_API_URL?: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}

declare module "@alptugidin/react-circular-progress-bar" {
    import type {FC} from "react";

    type SignPosition = "start" | "end";
    type StrokeLineCap = "butt" | "round" | "square";
    type FlatShape = "full" | "threequarters" | "half";
    type FontWeight = "normal" | "bold" | "bolder" | "lighter";

    type FlatProps = {
        progress: number;
        range?: {from: number; to: number};
        text?: string;
        sign?: {value: string; position: SignPosition};
        showValue?: boolean;
        showMiniCircle?: boolean;
        sx: {
            strokeColor: string;
            bgStrokeColor?: string;
            bgColor?: {value: string; transparency: string};
            barWidth: number;
            shape?: FlatShape;
            strokeLinecap?: StrokeLineCap;
            valueSize?: number;
            valueWeight?: FontWeight;
            valueColor?: string;
            textSize?: number;
            textWeight?: FontWeight;
            textColor?: string;
            loadingTime?: number;
            miniCircleColor?: string;
            miniCircleSize?: number;
            valueAnimation?: boolean;
            intersectionEnabled?: boolean;
        };
    };

    export const Flat: FC<FlatProps>;
}
