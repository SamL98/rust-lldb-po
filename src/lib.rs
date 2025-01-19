use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(DebugPrint)]
pub fn debug_print_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let name = input.ident;

    let expanded = quote! {
        use std::ffi::CString;

        impl #name {
            pub fn debug(&self) -> CString {
                CString::new(format!("{:?}", self).as_str()).unwrap()
            }
        }

        #[used]
        static DEBUG_METHOD: fn(&#name) -> CString = #name::debug;
    };

    TokenStream::from(expanded)
}
