import Layout from '../layouts/Main';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { MICHELANGELO } from '../utils/server';
import { postData } from '../utils/services';
import validator from 'validator';

const RegisterPage = () => {
    const { register, handleSubmit, errors } = useForm();

    const onSubmit = async ({ email, password, first_name, last_name }) => {
        const isEmail = validator.isEmail(email);
        const isPassword = validator.isStrongPassword(password);
        if (isEmail && isPassword) {
            await postData(`${MICHELANGELO}/api/accounts/register`, {
                username: email,
                email: email,
                password: password,
                first_name: first_name,
                last_name: last_name,
            });
        }
    };

    return (
        <Layout>
            <section className="form-page">
                <div className="container">
                    <div className="back-button-section">
                        <Link href="/products">
                            <a>
                                <i className="icon-left"></i> Back to store
                            </a>
                        </Link>
                    </div>

                    <div className="form-block">
                        <h2 className="form-block__title">
                            Create an account and discover the benefits
                        </h2>
                        <p className="form-block__description">
                            Lorem Ipsum is simply dummy text of the printing and
                            typesetting industry. Lorem Ipsum has been the
                            industry's standard dummy text ever since the 1500s
                        </p>

                        <form
                            className="form"
                            onSubmit={handleSubmit(onSubmit)}
                        >
                            <div className="form__input-row">
                                <input
                                    className="form__input"
                                    placeholder="First Name"
                                    name="first_name"
                                    type="text"
                                    ref={register()}
                                />
                            </div>

                            <div className="form__input-row">
                                <input
                                    className="form__input"
                                    placeholder="Last Name"
                                    name="last_name"
                                    type="text"
                                    ref={register()}
                                />
                            </div>

                            <div className="form__input-row">
                                <input
                                    className="form__input"
                                    placeholder="email"
                                    type="text"
                                    name="email"
                                    ref={register({
                                        required: true,
                                        pattern:
                                            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
                                    })}
                                />

                                {errors.email &&
                                    errors.email.type === 'required' && (
                                        <p className="message message--error">
                                            This field is required
                                        </p>
                                    )}

                                {errors.email &&
                                    errors.email.type === 'pattern' && (
                                        <p className="message message--error">
                                            Please write a valid email
                                        </p>
                                    )}
                            </div>

                            <div className="form__input-row">
                                <input
                                    className="form__input"
                                    type="password"
                                    placeholder="Password"
                                    name="password"
                                    ref={register({ required: true })}
                                />
                                {errors.password &&
                                    errors.password.type === 'required' && (
                                        <p className="message message--error">
                                            This field is required
                                        </p>
                                    )}
                            </div>

                            <div className="form__info">
                                <div className="checkbox-wrapper">
                                    <label
                                        htmlFor="check-signed-in"
                                        className={`checkbox checkbox--sm`}
                                    >
                                        <input
                                            name="signed-in"
                                            type="checkbox"
                                            id="check-signed-in"
                                        />
                                        <span className="checkbox__check"></span>
                                        <p>
                                            I agree to the Google Terms of
                                            Service and Privacy Policy
                                        </p>
                                    </label>
                                </div>
                            </div>

                            <button
                                type="submit"
                                className="btn btn--rounded btn--yellow btn-submit"
                            >
                                Sign up
                            </button>

                            <p className="form__signup-link">
                                <Link href="/login">
                                    <a href="#">Are you already a member?</a>
                                </Link>
                            </p>
                        </form>
                    </div>
                </div>
            </section>
        </Layout>
    );
};

export default RegisterPage;
