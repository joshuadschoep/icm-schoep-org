import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { useFormContext } from "react-hook-form";

export const Selection = () => {
  const { control } = useFormContext();

  return (
    <FormField
      control={control}
      name="method"
      render={({ field }) => (
        <FormItem>
          <FormLabel className="mx-auto md:m-0">Calculation Method</FormLabel>
          <FormControl>
            <RadioGroup
              onValueChange={field.onChange}
              defaultValue={field.value}
            >
              <div className="flex items-center gap-6">
                <FormItem className="flex items-center">
                  <FormControl>
                    <RadioGroupItem value="malmuth" />
                  </FormControl>
                  <FormLabel className="font-normal">
                    Malmuth-Harville
                  </FormLabel>
                </FormItem>
                <FormItem className="flex items-center">
                  <FormControl>
                    <RadioGroupItem value="tysen" />
                  </FormControl>
                  <FormLabel className="font-normal">Tysen</FormLabel>
                </FormItem>
              </div>
            </RadioGroup>
          </FormControl>
        </FormItem>
      )}
    />
  );
};
